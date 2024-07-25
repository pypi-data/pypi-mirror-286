import subprocess
import secure_pdf
import os

def main() -> None:
    app_path = secure_pdf.start.__file__.rsplit(os.sep,1)[0]
    subprocess.run(["streamlit", "run", f"{app_path}{os.sep}app.py"])

if __name__ == "__main__":
    main()
