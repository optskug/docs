Based off of share-and-enjoy's and Rez's guide on Discord.

**This is a WIKI, press Edit on this page to edit and save.**

The instructions can and will change and are volatile. Please report and discuss any issues in the #toyota-security channel on the comma.ai Discord. The invite to that discord is at https://discord.comma.ai. Once joined, make sure to answer any prompts you see in the Discord to gain full access. Once that is answered, this link will work to get you to #toyota-security: https://discord.com/channels/469524606043160576/905950538816978974

Additionally, you may be interested in the latest news and history, so see this discussion: https://github.com/commaai/openpilot/discussions/19932

INSTRUCTIONS STATUS: WIP 🚧

---

1. Start off with the installation guide here:

   https://comma.ai/setup/comma-3x

2. Then once you get your Comma powered up, you'll connect it to your Wi-Fi network.

3. Install "Custom Software:
    - When it asks you to enter a URL for "Custom Software", first try: `https://installer.comma.ai/pd0wm/rav4-prime`
    - If you installation hangs and then restarts, try: `https://smiskol.com/fork/pd0wm/rav4-prime`

4. Get SSH setup on the device:
   * Before you start (Both): https://github.com/commaai/openpilot/wiki/SSH#before-you-start
   * macOS: https://github.com/commaai/openpilot/wiki/SSH#option-2mac---pre-installed-openssh-client-on-macos
   * Windows: https://github.com/commaai/openpilot/wiki/SSH#option-2---pre-installed-openssh-client-on-windows-10-and-up

5. Download Willem's secoc GitHub folder:
    - SSH back into your Comma device:
      ```sh
      ssh comma@"your Comma IP" enter comma for the login
      ```
    - Clone the repository:
      ```sh
      git clone https://github.com/I-CAN-hack/secoc
      ```

6. Kill openpilot:
    - Enter the following command:
      ```sh
      pkill -f openpilot
      ```
    - The Comma should display just the splash screen with the Comma logo.

7. Put the car into "Ignition on" mode but with "Not Ready to Drive":
    - Slow press the "Power" button twice WITHOUT pressing the brake pedal.
    - ![PXL_20240718_234619671 MP](https://github.com/user-attachments/assets/4970e82e-e7df-471f-9896-ba532509793d)


8. Run the `extract_keys.py` script:
    - Navigate to the secoc directory:
      ```sh
      cd secoc
      ```
    - Run the script:
      ```sh
      ./extract_keys.py
      ```

9. Edit the script if you get an "Unexpected application version!" error:
    - Open the script for editing:
      ```sh
      nano -l /data/openpilot/secoc/extract_keys.py
      ```
    - Comment out lines 75-77 and 90-92 by adding a `#` at the beginning of each line:
      ```python
      # if app_version not in APPLICATION_VERSIONS:
      #    print("Unexpected application version!", app_version)
      #    exit(1)
      #
      # if bl_version != APPLICATION_VERSIONS[app_version]:
      #    print("Unexpected bootloader version!", bl_version)
      #    exit(1)
      ```
    - Save and exit the editor (Ctrl+X, then Y, then Enter).
    - Run the script again:
      ```sh
      ./extract_keys.py
      ```

10. Manually add the key to params (if needed):
    - Use the following command to manually change the keys:
      ```sh
      echo -n "your key here" > /data/params/d/SecOCKey
      ```

11. Fingerprinting (if the car is not recognized):
    - Follow the guide on fingerprinting:
      https://github.com/commaai/openpilot/wiki/Fingerprinting
    - Locate the necessary ECU codes.
    - Add the ECU codes to `fingerprints.py`:
      ```sh
      nano /data/openpilot/selfdrive/car/toyota/fingerprints.py
      ```
    - Scroll down to the `CAR.TOYOTA_RAV4_PRIME` section and enter your corresponding ECU codes:
      ```python
      },
      CAR.TOYOTA_RAV4_PRIME: {
        (Ecu.engine, 0x700, None): [
          b'\x01896634AJ7000\x00\x00\x00\x00',
          b'\x018966342S7000\x00\x00\x00\x00',
        ],
        (Ecu.abs, 0x7b0, None): [
          b'\x01F15264284100\x00\x00\x00\x00',
          b'\x01F15264228300\x00\x00\x00\x00',
        ],
        (Ecu.eps, 0x7a1, None): [
          b'\x018965B4233100\x00\x00\x00\x00',
          b'\x018965B4209000\x00\x00\x00\x00',
        ],
        (Ecu.fwdRadar, 0x750, 0xf): [
          b'\x018821F6201300\x00\x00\x00\x00',
          b'\x018821F3301400\x00\x00\x00\x00',
        ],
        (Ecu.fwdCamera, 0x750, 0x6d): [
          b'\x028646F4210100\x00\x00\x00\x008646G3305000\x00\x00\x00\x00',
          b'\x028646F4205200\x00\x00\x00\x008646G4202000\x00\x00\x00\x00',
        ],
      ```

12. Disable updates

    ```sh
    echo -en "1" > /data/params/d/DisableUpdates
    ```

12. Reboot the device:
    - Enter the reboot command:
      ```sh
      sudo reboot
      ```

13. Now, you should be ready to go!!!