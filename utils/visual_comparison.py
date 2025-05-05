import logging
import os
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageChops

logger = logging.getLogger(__name__)

class VisualComparison:
    def __init__(self, baseline_dir: str, diff_dir: str):
        self.baseline_dir = Path(baseline_dir)
        self.diff_dir = Path(diff_dir)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.diff_dir.mkdir(parents=True, exist_ok=True)

    def compare_screenshots(self, actual_screenshot: bytes, screenshot_name: str) -> Tuple[bool, str]:
        baseline_path = self.baseline_dir / f"{screenshot_name}.png"
        diff_path = self.diff_dir / f"{screenshot_name}_diff.png"
        actual_path = self.diff_dir / f"{screenshot_name}_actual.png"

        # Save actual screenshot
        with open(actual_path, "wb") as f:
            f.write(actual_screenshot)

        # If baseline doesn't exist, create it
        if not baseline_path.exists():
            logger.info(f"Creating baseline image: {baseline_path}")
            with open(baseline_path, "wb") as f:
                f.write(actual_screenshot)
            return True, "Baseline created"

        # Compare images
        actual_image = Image.open(actual_path)
        baseline_image = Image.open(baseline_path)

        if actual_image.size != baseline_image.size:
            logger.error(f"Size mismatch: Baseline {baseline_image.size} vs Actual {actual_image.size}")
            return False, "Size mismatch"

        diff = ImageChops.difference(actual_image, baseline_image)
        if diff.getbbox():
            # Save diff image
            diff.save(diff_path)
            logger.error(f"Visual difference detected. Diff saved to: {diff_path}")
            return False, f"Visual difference detected. Check diff at {diff_path}"

        return True, "Images match"

    def update_baseline(self, screenshot: bytes, screenshot_name: str) -> None:
        """Update or create baseline image"""
        baseline_path = self.baseline_dir / f"{screenshot_name}.png"
        with open(baseline_path, "wb") as f:
            f.write(screenshot)
        logger.info(f"Updated baseline image: {baseline_path}")