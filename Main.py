import io
import streamlit as st
import ezdxf
from ezdxf.enums import TextEntityAlignment

def generate_bs5839_dxf():
    """Generates the updated BS 5839 DXF document and returns it as a BytesIO buffer."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()

    # 1. Setup BS 5839 Standard Layers
    layers = {
        "FIRE_DETECTION": 1,  # Red (Detectors)
        "FIRE_MCP": 1,        # Red (Call Points)
        "FIRE_ALARM": 1,      # Red (Sounders, VADs & Outstations)
        "FIRE_MODULES": 6,    # Magenta (Active Interfaces)
        "FIRE_PANEL": 5,      # Blue (Panels / Control Gear)
        "FIRE_DISUSED": 8,    # Dark Grey (Redundant / Legacy Wired Equipment)
        "FIRE_TEXT": 7        # White/Black (Labels & Addresses)
    }
    for name, color in layers.items():
        layer = doc.layers.new(name)
        layer.color = color

    r = 150.0  # Base radius (300mm diameter footprint)

    # -------------------------------------------------------------------------
    # BLOCK 1: Optical Smoke Detector
    # -------------------------------------------------------------------------
    opt_block = doc.blocks.new(name="BS5839_OPTICAL")
    opt_block.add_circle((0, 0), radius=r, dxfattribs={"layer": "FIRE_DETECTION", "lineweight": 35})
    opt_block.add_text("S", height=180, dxfattribs={"layer": "FIRE_DETECTION", "style": "Standard"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # BLOCK 2: Heat Detector
    # -------------------------------------------------------------------------
    heat_block = doc.blocks.new(name="BS5839_HEAT")
    heat_block.add_circle((0, 0), radius=r, dxfattribs={"layer": "FIRE_DETECTION", "lineweight": 35})
    heat_block.add_text("H", height=180, dxfattribs={"layer": "FIRE_DETECTION", "style": "Standard"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # BLOCK 3: Manual Call Point
    # -------------------------------------------------------------------------
    mcp_block = doc.blocks.new(name="BS5839_MCP")
    half = 150.0
    mcp_block.add_lwpolyline(
        [(-half, -half), (half, -half), (half, half), (-half, half)],
        close=True,
        dxfattribs={"layer": "FIRE_MCP", "lineweight": 35}
    )
    i_half = half * 0.4
    mcp_block.add_lwpolyline(
        [(-i_half, -i_half), (i_half, -i_half), (i_half, i_half), (-i_half, i_half)],
        close=True,
        dxfattribs={"layer": "FIRE_MCP", "lineweight": 25}
    )

    # -------------------------------------------------------------------------
    # BLOCK 4: Wall/Standalone Sounder / VAD
    # -------------------------------------------------------------------------
    snd_block = doc.blocks.new(name="BS5839_SOUNDER_VAD")
    snd_block.add_circle((0, 0), radius=r, dxfattribs={"layer": "FIRE_ALARM", "lineweight": 35})
    ray_len = 80.0
    snd_block.add_line((r, 0), (r + ray_len, 0), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    snd_block.add_line((-r, 0), (-r - ray_len, 0), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    snd_block.add_line((0, r), (0, r + ray_len), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    snd_block.add_line((0, -r), (0, -r - ray_len), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})

    # -------------------------------------------------------------------------
    # BLOCK 5: Sounder / VAD Base (Detector + Base Sounder Combination)
    # -------------------------------------------------------------------------
    base_snd_block = doc.blocks.new(name="BS5839_SOUNDER_VAD_BASE")
    base_snd_block.add_circle((0, 0), radius=r, dxfattribs={"layer": "FIRE_ALARM", "lineweight": 35})
    ray_len = 70.0
    base_snd_block.add_line((r, 0), (r + ray_len, 0), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    base_snd_block.add_line((-r, 0), (-r - ray_len, 0), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    base_snd_block.add_line((0, r), (0, r + ray_len), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    base_snd_block.add_line((0, -r), (0, -r - ray_len), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    base_snd_block.add_circle((0, 0), radius=r * 0.65, dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})

    # -------------------------------------------------------------------------
    # BLOCK 6: Sounder Outstation / Emergency Voice Communication (EVC)
    # -------------------------------------------------------------------------
    outstation_block = doc.blocks.new(name="BS5839_OUTSTATION")
    w, h = 320.0, 320.0
    outstation_block.add_lwpolyline(
        [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)],
        close=True,
        dxfattribs={"layer": "FIRE_ALARM", "lineweight": 35}
    )
    outstation_block.add_text("T", height=160, dxfattribs={"layer": "FIRE_ALARM"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # BLOCK 7: Addressable Fire Alarm Panel (FAP-A)
    # -------------------------------------------------------------------------
    panel_addr = doc.blocks.new(name="BS5839_PANEL_ADDR")
    pw, ph = 600.0, 400.0
    panel_addr.add_lwpolyline(
        [(-pw/2, -ph/2), (pw/2, -ph/2), (pw/2, ph/2), (-pw/2, ph/2)],
        close=True,
        dxfattribs={"layer": "FIRE_PANEL", "lineweight": 35}
    )
    off = 30.0
    panel_addr.add_lwpolyline(
        [(-pw/2 + off, -ph/2 + off), (pw/2 - off, -ph/2 + off), (pw/2 - off, ph/2 - off), (-pw/2 + off, ph/2 - off)],
        close=True,
        dxfattribs={"layer": "FIRE_PANEL", "lineweight": 20}
    )
    panel_addr.add_text("FAP-A", height=130, dxfattribs={"layer": "FIRE_PANEL"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # BLOCK 8: Conventional Fire Alarm Panel (FAP-C)
    # -------------------------------------------------------------------------
    panel_conv = doc.blocks.new(name="BS5839_PANEL_CONV")
    panel_conv.add_lwpolyline(
        [(-pw/2, -ph/2), (pw/2, -ph/2), (pw/2, ph/2), (-pw/2, ph/2)],
        close=True,
        dxfattribs={"layer": "FIRE_PANEL", "lineweight": 35}
    )
    panel_conv.add_text("FAP-C", height=130, dxfattribs={"layer": "FIRE_PANEL"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # BLOCK 9: Active Interface Module (I/O)
    # -------------------------------------------------------------------------
    mod_block = doc.blocks.new(name="BS5839_INTERFACE")
    mw, mh = 400.0, 250.0
    mod_block.add_lwpolyline(
        [(-mw/2, -mh/2), (mw/2, -mh/2), (mw/2, mh/2), (-mw/2, mh/2)],
        close=True,
        dxfattribs={"layer": "FIRE_MODULES", "lineweight": 35}
    )
    mod_block.add_text("I/O", height=120, dxfattribs={"layer": "FIRE_MODULES"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # BLOCK 10: Disused / Legacy I/O Unit (Wired but Unused)
    # -------------------------------------------------------------------------
    disused_block = doc.blocks.new(name="BS5839_IO_DISUSED")
    # Outer box on FIRE_DISUSED layer
    disused_block.add_lwpolyline(
        [(-mw/2, -mh/2), (mw/2, -mh/2), (mw/2, mh/2), (-mw/2, mh/2)],
        close=True,
        dxfattribs={"layer": "FIRE_DISUSED", "lineweight": 25}
    )
    # Diagonal strike-through cross
    disused_block.add_line((-mw/2, -mh/2), (mw/2, mh/2), dxfattribs={"layer": "FIRE_DISUSED", "lineweight": 20})
    disused_block.add_line((-mw/2, mh/2), (mw/2, -mh/2), dxfattribs={"layer": "FIRE_DISUSED", "lineweight": 20})
    # Centered designation
    disused_block.add_text("I/O (SPARE)", height=80, dxfattribs={"layer": "FIRE_DISUSED"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # Populate Modelspace Legend
    # -------------------------------------------------------------------------
    symbols = [
        ("BS5839_OPTICAL", "Optical Smoke Detector (S)"),
        ("BS5839_HEAT", "Heat Detector (H)"),
        ("BS5839_MCP", "Manual Call Point (MCP)"),
        ("BS5839_SOUNDER_VAD", "Sounder / VAD Beacon"),
        ("BS5839_SOUNDER_VAD_BASE", "Sounder / VAD Base Unit"),
        ("BS5839_OUTSTATION", "Sounder Outstation / EVC"),
        ("BS5839_PANEL_ADDR", "Addressable Fire Alarm Control Panel"),
        ("BS5839_PANEL_CONV", "Conventional Fire Alarm Control Panel"),
        ("BS5839_INTERFACE", "Input / Output Interface Module"),
        ("BS5839_IO_DISUSED", "Redundant / Disused I/O Unit (Wired)")
    ]

    y_pos = 0.0
    for block_name, label in symbols:
        msp.add_blockref(block_name, insert=(0, y_pos))
        msp.add_text(
            f"{label}", height=150, dxfattribs={"layer": "FIRE_TEXT"}
        ).set_placement((600, y_pos), align=TextEntityAlignment.MIDDLE_LEFT)
        
        msp.add_text(
            "L1-001", height=100, dxfattribs={"layer": "FIRE_TEXT"}
        ).set_placement((0, y_pos - 250), align=TextEntityAlignment.MIDDLE)

        y_pos -= 800.0

    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue().encode('utf-8')

# --- Streamlit UI ---
st.set_page_config(page_title="BS 5839 CAD Generator", page_icon="🧯", layout="centered")

st.title("🧯 BS 5839 Fire Alarm CAD Symbol Generator")
st.write("Generates an updated AutoCAD R2010 DXF library including disused/redundant wired I/O units.")

dxf_bytes = generate_bs5839_dxf()

st.download_button(
    label="📥 Download BS5839_Fire_Alarm_Library.dxf",
    data=dxf_bytes,
    file_name="BS5839_Fire_Alarm_Library.dxf",
    mime="application/dxf",
    use_container_width=True
)
