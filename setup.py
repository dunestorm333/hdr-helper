import re
import subprocess
import os

class Setup():
    def __init__(self):
        self.default_mode = None
        self.alt_rate = None
        self.alt_res_and_rate = None
        self.output_name = None

    def extract_display_info(self):
        # Run process, capture output as a string
        proc = subprocess.run(
            ["kscreen-doctor -o"],
            shell=True,
            capture_output=True,
            text=True
        )
        output = proc.stdout

        # Remove ANSI escape codes for clean regex matching
        output_clean = re.sub(r'\x1b\[[0-9;]*m', '', output)

        # Find all resolutions with flags
        resolutions = re.findall(r'\d+x\d+@\d+\S', output_clean)

        # Identify default display mode and alternatives
        for i in resolutions:
            if i.endswith('*'):
                self.default_mode = i
            if self.default_mode and i != self.default_mode:
                if i.startswith(self.default_mode.split('@')[0]):
                    self.alt_rate = i
                    break
                else:
                    self.alt_res_and_rate = i
                    

        # Remove asterisk from default
        if self.default_mode:
            self.default_mode = self.default_mode.strip('*')

        search_output = re.search(r'Output:\s*\d+\s+(\S+)', output_clean)

        # Extract and print output name
        if search_output:
            self.output_name = search_output.group(1)
            
    def print_display_info(self):
        print(f"Output Name: {self.output_name}")
        print(f"Default Mode: {self.default_mode}")
        print(f"Alternative Rate: {self.alt_rate}")
        print(f"Alternative Resolution and Rate: {self.alt_res_and_rate}")

    def edit_config_file(self):
        conf_file = "monitor.conf"
        if os.path.isfile(conf_file):
            with open(conf_file, "r") as file:
                lines = file.readlines()

            with open(conf_file, "w") as file:            
                for line in lines:
                    if "MONITOR=" in line:
                        line = line.replace("MONITOR=\n", f"MONITOR={self.output_name}\n")
                    elif "NATIVE_RES=" in line:
                        line = line.replace("NATIVE_RES=\n", f"NATIVE_RES={self.default_mode}\n")

                    # Prefer alt_rate if available, otherwise alt_res_and_rate
                    if "TEMP_RES=" in line:
                        if self.alt_rate:
                            line = line.replace("TEMP_RES=\n", f"TEMP_RES={self.alt_rate}\n")
                        elif self.alt_res_and_rate:
                            line = line.replace("TEMP_RES=\n", f"TEMP_RES={self.alt_res_and_rate}\n")
                        
                    file.write(line)
            


setup = Setup()
setup.extract_display_info()
#setup.print_display_info()
setup.edit_config_file()