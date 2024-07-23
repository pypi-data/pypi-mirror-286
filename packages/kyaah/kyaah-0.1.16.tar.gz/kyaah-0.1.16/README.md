# Kyaah

Kyaah abstract away cognitive over-head of sending SMTP, POP3, and IMAP mail, together with other mailing operations things like, mail with file, tokens etc.

[![Downloads Month Badge](https://static.pepy.tech/badge/kyaah/month)](https://pypi.org/project/kyaah)
[![License Badge](https://img.shields.io/pypi/l/kyaah.svg)](https://pypi.org/project/kyaah)
[![Supported Wheel Badge](https://img.shields.io/pypi/wheel/kyaah.svg)](https://pypi.org/project/kyaah)
[![Supported Versions Badge](https://img.shields.io/pypi/pyversions/kyaah.svg)](https://pypi.org/project/kyaah)

# Installation & Usage

First, you are recommended to create a virtual environment `python -m venv venv` and then activate it `source venv/bin/activate`, next install the library using:

```sh
    pip install kyaah
```

Wait for the installation to finish, basically the library was uploaded using `sdist` (Source Distribution) and `bdist_wheel` (Built Distribution).

After that, simply import the library and set payload, which include `sender`, `receiver`, `subject`, `body`, and `password` and lastly call the `send` method and pass the `payload` as a keyword just like the sample below:

```python
    import kyaah
        
    payload = dict(
        sender = "myemail@gmail.com",
        receiver = ["receiver@gmail.com"],
        subject = "Hellow world!",
        body = "Lorem ipsum dolor sit amet adipisicing elit, rerum voluptate ipsum volupt.",
        password = "*********",
    )

    kyaah.send(credentials=payload)
```

## Useful links

-   Documentations: https://kyaah.readthedocs.io
-   Repository: https://github.com/usmanmusa1920/kyaah
-   PYPI Release: https://pypi.org/project/kyaah
