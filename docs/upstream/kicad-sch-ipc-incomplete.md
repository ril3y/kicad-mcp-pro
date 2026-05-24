# Upstream KiCad gap: schematic IPC item-creation is partially implemented

**Target:** gitlab.com/kicad/code/kicad — file as an issue + optional MR

## Summary

Schematic `CreateItems` IPC requests sent to a running `eeschema` (built
from master, e.g. nightly `10.99.0.1059.g0895df3e3c`) return `ISC_OK` for
allowed item types but the resulting items render with **default-constructed
state** because two upstream code paths are incomplete:

1. `common/api/api_utils.cpp::TypeNameFromAny()` registers **zero**
   schematic proto types. Only board types appear in the `s_types` map.
2. `eeschema/sch_label.cpp::SCH_GLOBALLABEL::{Serialize,Deserialize}` are
   `UNIMPLEMENTED_FOR()` stubs. `SCH_LABEL::Deserialize()` reads `id` and
   `position` only — the `text` field is ignored.

## Reproduction

1. Build KiCad master (or use a nightly that contains commit `3dca4e0e38`).
2. Open any schematic in standalone `eeschema`.
3. Enable IPC: `~/.config/kicad/10.99/kicad_common.json` → `"api": { "enable_server": true }`.
4. From any kipy-equipped Python:

   ```python
   from kipy import KiCad
   from kipy.proto.common.commands.editor_commands_pb2 import CreateItems, CreateItemsResponse
   from kipy.proto.common.types import DocumentType
   from kipy.proto.schematic.schematic_types_pb2 import GlobalLabel, Line, SchematicLayer
   from kipy.util import pack_any

   k = KiCad()
   doc = list(k.get_open_documents(DocumentType.DOCTYPE_SCHEMATIC))[0]

   # Case A: GlobalLabel — accepted with ISC_OK, but text is dropped
   label = GlobalLabel()
   label.position.x_nm = 50_000_000
   label.position.y_nm = 50_000_000
   label.text.text.text = "HELLO"
   label.text.text.attributes.size.x_nm = 1_270_000
   label.text.text.attributes.size.y_nm = 1_270_000
   cmd = CreateItems()
   cmd.header.document.CopyFrom(doc)
   cmd.items.append(pack_any(label))
   resp = k._client.send(cmd, CreateItemsResponse)
   # → resp.created_items[0].status.code == ISC_OK
   # → eeschema renders an empty-text global label

   # Case B: Line — rejected outright
   line = Line()
   line.start.x_nm = 60_000_000
   line.start.y_nm = 50_000_000
   line.end.x_nm = 80_000_000
   line.end.y_nm = 50_000_000
   line.layer = SchematicLayer.LAYER_WIRE
   cmd = CreateItems()
   cmd.header.document.CopyFrom(doc)
   cmd.items.append(pack_any(line))
   resp = k._client.send(cmd, CreateItemsResponse)
   # → resp.created_items[0].status.code == ISC_INVALID_TYPE
   # → "Could not decode a valid type from type.googleapis.com/kiapi.schematic.types.Line"
   ```

## Required changes (sketch)

### 1. Register schematic types in `TypeNameFromAny`

```cpp
// common/api/api_utils.cpp:35
static const std::map<std::string, KICAD_T> s_types = {
    // ... existing board entries ...
    { "type.googleapis.com/kiapi.schematic.types.LocalLabel",        SCH_LABEL_T },
    { "type.googleapis.com/kiapi.schematic.types.GlobalLabel",       SCH_GLOBAL_LABEL_T },
    { "type.googleapis.com/kiapi.schematic.types.HierarchicalLabel", SCH_HIER_LABEL_T },
    { "type.googleapis.com/kiapi.schematic.types.DirectiveLabel",    SCH_DIRECTIVE_LABEL_T },
    { "type.googleapis.com/kiapi.schematic.types.Line",              SCH_LINE_T },
    { "type.googleapis.com/kiapi.schematic.types.Junction",          SCH_JUNCTION_T },
    { "type.googleapis.com/kiapi.schematic.types.NoConnect",         SCH_NO_CONNECT_T },
    { "type.googleapis.com/kiapi.schematic.types.Text",              SCH_TEXT_T },
    { "type.googleapis.com/kiapi.schematic.types.TextBox",           SCH_TEXTBOX_T },
    { "type.googleapis.com/kiapi.schematic.types.Shape",             SCH_SHAPE_T },
};
```

### 2. Complete `SCH_LABEL::{Serialize,Deserialize}` to handle text

```cpp
// eeschema/sch_label.cpp:1612
void SCH_LABEL::Serialize( google::protobuf::Any& aContainer ) const
{
    kiapi::schematic::types::LocalLabel label;
    label.mutable_id()->set_value( m_Uuid.AsStdString() );
    kiapi::common::PackVector2( *label.mutable_position(), GetPosition() );
    // NEW:
    auto& inner = *label.mutable_text()->mutable_text();
    inner.set_text( GetText().ToStdString() );
    // serialize text attributes (size, font, etc.) — see EDA_TEXT helpers
    aContainer.PackFrom( label );
}

bool SCH_LABEL::Deserialize( const google::protobuf::Any& aContainer )
{
    kiapi::schematic::types::LocalLabel label;
    if( !aContainer.UnpackTo( &label ) ) return false;
    const_cast<KIID&>( m_Uuid ) = KIID( label.id().value() );
    SetPosition( kiapi::common::UnpackVector2( label.position() ) );
    // NEW:
    if( label.has_text() && label.text().has_text() )
        SetText( wxString::FromUTF8( label.text().text().text() ) );
    return true;
}
```

### 3. Implement `SCH_GLOBALLABEL::{Serialize,Deserialize}` (currently `UNIMPLEMENTED_FOR`)

```cpp
// eeschema/sch_label.cpp:2035
void SCH_GLOBALLABEL::Serialize( google::protobuf::Any& aContainer ) const
{
    kiapi::schematic::types::GlobalLabel label;
    label.mutable_id()->set_value( m_Uuid.AsStdString() );
    kiapi::common::PackVector2( *label.mutable_position(), GetPosition() );
    auto& inner = *label.mutable_text()->mutable_text();
    inner.set_text( GetText().ToStdString() );
    aContainer.PackFrom( label );
}

bool SCH_GLOBALLABEL::Deserialize( const google::protobuf::Any& aContainer )
{
    kiapi::schematic::types::GlobalLabel label;
    if( !aContainer.UnpackTo( &label ) ) return false;
    const_cast<KIID&>( m_Uuid ) = KIID( label.id().value() );
    SetPosition( kiapi::common::UnpackVector2( label.position() ) );
    if( label.has_text() && label.text().has_text() )
        SetText( wxString::FromUTF8( label.text().text().text() ) );
    return true;
}
```

### 4. Same pattern for `SCH_HIERLABEL`, `SCH_LINE`, `SCH_JUNCTION`, `SCH_NO_CONNECT`

## Impact on third-party tooling

Until this is fixed, the schematic IPC framework that landed in commit
`3dca4e0e38` ("API: implement schematic item creation", Jon Evans,
2026-04-07) functions as a no-op for any third-party tool — including
plugins that use the Python `kipy` package — because items can be
"created" but cannot carry text, geometry, or arrangement.

The defensive-validation half of that commit IS effective: stale 10.0.x
behaviour was to crash eeschema on malformed input; master correctly
returns `AS_BAD_REQUEST` or default-constructed items. Completing the
serdes is the remaining piece.

## Status

- Architecture in `kicad-mcp` is in place (PR #26 client + PR #27 runtime
  gate). The gate routes to a hardened file-based path as long as the
  upstream serdes is incomplete; it transparently flips to IPC once
  upstream lands the missing pieces.
- A working sanity probe lives at `scripts/sch_ipc_sanity.py` in the
  `kicad-mcp` fork — reproduces both case A and case B above.
