from io import BytesIO

from PIL import Image

from services.ai_service import AIService


def test_analyze_crop_image_identifies_leaf_spot_and_instructions():
    image = Image.new("RGB", (200, 200), color=(90, 120, 60))
    for x in range(30, 170):
        for y in range(30, 170):
            if (x - 100) ** 2 + (y - 100) ** 2 < 2200:
                image.putpixel((x, y), (140, 70, 30))

    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    result = AIService().analyze_crop_image(image_bytes, crop_name="Tomato", user_notes="brown lesions on leaves", language="en")

    assert result["disease"] == "Leaf Spot"
    assert "instructions" in result
    assert any(keyword in result["instructions"].lower() for keyword in ["remove", "spray", "water", "avoid"])
