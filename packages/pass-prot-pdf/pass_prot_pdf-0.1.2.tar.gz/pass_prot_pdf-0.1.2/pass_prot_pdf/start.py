import subprocess
import pass_prot_pdf

def main() -> None:
    print("------------------")
    print(pass_prot_pdf.app.__file__)
    subprocess.run(["streamlit", "run", "pass_prot_pdf/app.py"])

if __name__ == "__main__":
    main()
