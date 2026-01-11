# Simple web Network Attached storage

## How it works

This is a project that allows you to create a url that can be used to share files on your local are network or across the internet with [advanced](#advance) setup, simple to use just running the script on a terminal window setting the root path, port and runtime else default to `current path`, a `random dynamic port` and `15 minutes` as runtime.

## How to install

> NOTE: Ensure you have python and git installed before you continue, **no additional python modules are required.** I'll also be assuming you are doing everything from a terminal window.

- *Clone the repo and move into the directory.*

```shell
git clone https://github.com/thread101/simple-home-lab-web-host.git
cd simple-home-lab-web-host
```

- *Run the script `NAS-server.py`.*

```shell
# Unix/Linux/Macs run
python3 NAS-server.py
```

```shell
# ms windows
python NAS-server.py
```

> This will create a url to the current directory with a random dynamic port and run for 15 minutes.

![output](/resources/output.png)

- *On Linux you can also run.*

```shell
chmod +x NAS-server.py
./NAS-server.py
```

- *The script also takes parameters. `path`, `port` and `runtime` respectively.*

```shell
# Unix/Linux/Macs run
python3 NAS-server.py /home/ 8080 10
```

```shell
# ms windows
python NAS-server.py C: 8080 10
```

> This takes the path parameter followed by the port and finally the runtime in minute, time can also be taken as floating point.

- *To open the link from another machine on your local area network just [find your device's ip address](https://www.wikihow.com/Find-Out-Your-IP-Address) and replace `localhost` with your ip say `192.168.43.136` to `http://192.168.43.136:8080`.*

- *You can visit the link and you should see such an interface.*

![web interface](/resources/web-interface.png)

- *To download press the download section.*

- *If you want to closing the connection before the elapse time press `ctrl+c` which will close the port and terminate the connection.*

> NOTE: If a directory contains html file and is clicked this renders the page on the browser, `index.html` are also opened by default.

<details id="advance">
<summary style="color: blue;">share over the internet</summary>

---

### To share over the internet you need to tunnel your connection to a remote server also known as port forwarding

*There are couple of methods, popular ones os using tools like `ngrok`, `localxpose` or `cloudflared`.*

*For simplicity I'll demonstrate using `cloudflared` since it doesn't require an account.*

- [Download](https://github.com/cloudflare/cloudflared/releases) and install your operating system's cloudflared executable.

- Run the `NAS-server.py` script normally from one terminal and open a separate one and run.

```shell
cloudflared tunnel --url=http://localhost:8080
```

![cloudflared output](/resources/cloudflared-output.png)

> Of course you have to use the url from the script if you did not specify the port.

- *You can now share the provided link `https://...-trycloudflare.com` to a friend and he can then connect and download the files you are sharing.*

> NOTE: The link is not consistent and you may be assigned a new link if you restart your cloudflared connection. Share this link with trusted individuals for security purposes.

- *`ctrl+c` to close the cloudflared connection, **for advanced setup you can go through [cloudflared documentation](https://developers.cloudflare.com/fundamentals/account/create-account/) and create an account to get your own domain**.*

- *For more info on the tool run `cloudflared --help` on your commandline or [visit](https://github.com/cloudflare/cloudflared/releases) their github repo.*

---

</details>

## Modification

- *Feel free to mod the `html`, and `css`  template in the `Web` directory, You can also embed `javascript` but will have to go under script tag in the html.*

### Hope you found it useful 😌

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?hosted_button_id=YOUR_BUTTON_ID)
