# Interactive Prototyping: The Clock of Pi

**Collaborators:** Vasudha Devkota  
**Acknowledgments & Influences:** 
- Course Instructors & TAs for setup guidance
- Open-source Adafruit MiniPiTFT / ST7789 CircuitPython libraries
- Generative AI assistance for Markdown formatting and script refinement

---

## Prep

- [x] Lab 2 GitHub repo updated and synced.
- [x] Parts inventory updated in `partslist.md`.
- [x] Raspberry Pi OS image flashed and booted successfully.

---

## Part A. Connect to your Pi
- Connected to Raspberry Pi via SSH over local network.
- Virtual environment (`venv`) created and activated.
- Configured GitHub `user.name`, `user.email`, and Personal Access Token (PAT) for authenticated pushing.

---

## Part B. Command Line Clock
- Cloned repository to `~/Interactive-Lab-Hub/Lab 2/`.
- Installed dependencies via `pip install -r requirements.txt`.
- Successfully ran `cli_clock.py` to print system time to terminal.

---

## Part C. Set up your RGB Display

### Hardware Setup & Testing

1. **Physical Enclosure & Component Prep:**
   ![Anatomical Heart Mold Prep](IMG_7261.JPG)
   https://drive.google.com/file/d/1kHAlO2viuLWQ0oJ0r-ydmFvkCOZ48SyJ/view?usp=drive_link

3. **Screen Test & Service Verification:**
   ![Pi Screen Service with MAC Address](piscreen_mac_address.jpg)
https://drive.google.com/file/d/1Bdy0pVBPvd7tgy4YtcwtGzWrggVfPs9e/view?usp=sharing
---

## Part D. Display Clock Demo
- Modified `screen_clock.py` to output live time onto the MiniPiTFT screen using `PIL` image drawing functions and custom typography.

---

## Part E. Sketching & Brainstorming (Part 1)

### Concept: *Anatomical Chroma Heart Clock*
Instead of traditional digits or clock hands, this design measures time through atmospheric light shift. An illuminated, translucent anatomical heart serves as the central visual centerpiece. 

- **Unit of Time:** Diurnal color shift (Dawn/Day/Dusk progression).
- **Light Behavior:** 
  - **Morning / Early Day:** Starts as a bright, clear white illumination, symbolizing fresh start and peak daylight[
  - **Evening / Late Day:** Gradually shifts into a deep blue hue as night approaches, reflecting circadian transition and wind-down time

### Interaction & System Storyboard

```text
  [ Time of Day / System Clock ]
                │
                ▼
      [ Read System Time ]
                │
                ▼
  [ Interpolate RGB Color State ]
  ( White: 08:00 -> Blue: 20:00 )
                │
                ▼
   [ Drive RGB Display / Light ]
                │
                ▼
 [ Translucent Heart Enclosure Glows ]
