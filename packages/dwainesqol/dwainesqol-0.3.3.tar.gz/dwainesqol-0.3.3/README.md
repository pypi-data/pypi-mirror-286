


# Qol tools by Dwaine Glover

### Email me at `GloverDwaine@Gmail.com` for suggestions

Ever found yourself screaming at your computer because doing simple tasks feels like trying to explain quantum physics to a toddler? Yeah, we have all been there. That is why this module exists. I created this shitshow of a module to take the everyday pain-in-the-ass tasks and make them a little less soul-crushing. 


<br>

# `msgbox()` 


### What the Fuck is This?

The `msgbox()`  is your fucking way to show a goddamn message box in Windows using Python. If you want to waste time annoying people with pop-up boxes, this is your shit.

### How the Hell Do You Use It?

Instantiate the `msgbox()`  with the title, message, and the type of box you want to display.

### Usage Examples



#### Basic OK Box

```python
msgbox("Title", "This is a fucking OK message box", "MB_OK")
```

#### OK/Cancel Box

```python
msgbox("Title", "This is an OK/Cancel box, deal with it", "MB_OKCXL")
```

#### Yes/No/Cancel Box

```python
msgbox("Title", "Make up your fucking mind! Yes, No, or Cancel?", "MB_YESNOCXL")
```

#### Yes/No Box

```python
msgbox("Title", "Just a simple Yes or No, how hard can it be?", "MB_YESNO")
```

### Icons? Fuck Yeah!

#### Exclamation Icon

```python
msgbox("Warning", "Something might be fucked up!", "ICON_EXCLAIM")
```

#### Information Icon

```python
msgbox("Info", "Here's some useless info for you.", "ICON_INFO")
```

#### Stop Icon

```python
msgbox("Error", "You really fucked up now!", "ICON_STOP")
```

### Note

The funtion runs on Windows because it uses `ctypes` to access the Windows API. If you are not on Windows, fuck off and find another solution.


<br>

# `bsod()`



### What the Fuck is This?

The `bsod()` class is your quick and dirty way to induce a Blue Screen of Death (BSOD) on a Windows machine. Yep, you heard that right. This is the ultimate "nuke it from orbit" tool for when you just want to watch the world burn or maybe you are just a sadistic coder who gets their kicks from watching systems crash and burn. Whatever your twisted reason, the `bsod()`  is here for you. Use it responsibly, or not, I am not your fucking mom.



> Disclaimer: I am not responsible for any damage, data loss, or general chaos that ensues from using this.



## How the Hell Do You Use It?


Simply use `msgbox()` to trigger a BSOD:

```python
bsod()
```

That's it. No fancy parameters, no bullshit. Just instant system meltdown.

### Note

The funtion runs on Windows because it uses `ctypes` to access the Windows API. If you are not on Windows, fuck off and find another solution.



<br>
<br>

## Work in progress
### `clipbored()`
### `scroll()`
### and more... 
#

