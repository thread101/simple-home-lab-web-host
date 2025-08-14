import subprocess as sb
import os

if __name__ == "__main__":  
    import functs as exts

else:
    import bin.functs as exts

@exts.critical
def run_command(cmd):
    if "cd " in cmd:
        directory = cmd[cmd.index("cd ")+3:]
        try:
            os.chdir(directory)
            result = ""
        
        except FileNotFoundError as e:
            result = f"{e}"
        
    else:
        r = sb.run(cmd.split(), text=True, capture_output=True)

        if r.returncode == 0:
            result = f"{r.stdout}"
        
        else:
            result = f"{r.stderr}"

    return f"{result}"


def format_terminal(text):
    text = text if "\n" in text else f"\n{text}"
    width = os.get_terminal_size().columns
    prompt = text.split("\n")[-1]
    texts = text.split("\n")[:-1]
    size = max([len(i) for i in texts])
 
    t = "\r"
    for _txt in texts:
        txt = f"{_txt}{' '*(size-len(_txt))}  "
        if len(t.split('\n')[-1]) + len(txt) <= width:
            t += txt

        else:
            t += f"\n{txt}"

    return t + "\n\n" + prompt

