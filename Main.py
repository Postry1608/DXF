import io
import streamlit as st
import ezdxf
from ezdxf.enums import TextEntityAlignment

def generate_bs5839_dxf():
    """Generates the BS 5839 DXF document and returns it as a BytesIO buffer."""
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()

    # 1. Setup BS 5839 Standard Layers
    layers = {
        "FIRE_DETECTION": 1,  # Red
        "FIRE_MCP": 1,        # Red
        "FIRE_ALARM": 1,      # Red
        "FIRE_MODULES": 6,    # Magenta
        "FIRE_TEXT": 7        # White/Black
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
    # BLOCK 3: Multi-Sensor / Opto-Heat
    # -------------------------------------------------------------------------
    multi_block = doc.blocks.new(name="BS5839_MULTISENSOR")
    multi_block.add_circle((0, 0), radius=r, dxfattribs={"layer": "FIRE_DETECTION", "lineweight": 35})
    multi_block.add_line((-r, 0), (r, 0), dxfattribs={"layer": "FIRE_DETECTION", "lineweight": 25})
    multi_block.add_text("O", height=100, dxfattribs={"layer": "FIRE_DETECTION"}).set_placement(
        (0, 60), align=TextEntityAlignment.MIDDLE
    )
    multi_block.add_text("H", height=100, dxfattribs={"layer": "FIRE_DETECTION"}).set_placement(
        (0, -60), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # BLOCK 4: Manual Call Point
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
    # BLOCK 5: Sounder / VAD
    # -------------------------------------------------------------------------
    snd_block = doc.blocks.new(name="BS5839_SOUNDER_VAD")
    snd_block.add_circle((0, 0), radius=r, dxfattribs={"layer": "FIRE_ALARM", "lineweight": 35})
    ray_len = 80.0
    snd_block.add_line((r, 0), (r + ray_len, 0), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    snd_block.add_line((-r, 0), (-r - ray_len, 0), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    snd_block.add_line((0, r), (0, r + ray_len), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})
    snd_block.add_line((0, -r), (0, -r - ray_len), dxfattribs={"layer": "FIRE_ALARM", "lineweight": 25})

    # -------------------------------------------------------------------------
    # BLOCK 6: Interface Module
    # -------------------------------------------------------------------------
    mod_block = doc.blocks.new(name="BS5839_INTERFACE")
    w, h = 400.0, 250.0
    mod_block.add_lwpolyline(
        [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)],
        close=True,
        dxfattribs={"layer": "FIRE_MODULES", "lineweight": 35}
    )
    mod_block.add_text("I/O", height=120, dxfattribs={"layer": "FIRE_MODULES"}).set_placement(
        (0, 0), align=TextEntityAlignment.MIDDLE
    )

    # -------------------------------------------------------------------------
    # Populate Modelspace Legend
    # -------------------------------------------------------------------------
    symbols = [
        ("BS5839_OPTICAL", "Optical Smoke Detector (S)"),
        ("BS5839_HEAT", "Heat Detector (H)"),
        ("BS5839_MULTISENSOR", "Multi-Sensor Detector (O/H)"),
        ("BS5839_MCP", "Manual Call Point (MCP)"),
        ("BS5839_SOUNDER_VAD", "Sounder / VAD Beacon"),
        ("BS5839_INTERFACE", "Input / Output Interface Module")
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

    # Write DXF to binary stream buffer
    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue().encode('utf-8')

# --- Streamlit UI App ---
st.set_page_config(page_title="BS 5839 CAD Generator", page_icon="🧯", layout="centered")

st.title("🧯 BS 5839 Fire Alarm CAD Symbol Generator")
st.write("Generates a standard AutoCAD R2010 DXF library with pre-configured layers and blocks.")

# Generate file in memory
dxf_bytes = generate_bs5839_dxf()

# Direct Download Button
st.download_button(
    label="📥 Download BS5839_Fire_Alarm_Library.dxf",
    data=dxf_bytes,
    file_name="BS5839_Fire_Alarm_Library.dxf",
    mime="application/dxf",
    use_container_width=True
)
