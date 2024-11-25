<div align="center">
   <img src="https://user-images.githubusercontent.com/22733958/183041432-cf6cc6f4-3a6f-4070-91a8-d0a7f7abf59f.JPG" width="600">
</div>

<div align="center">
   SKILLPOINTER
   PROYECTO FINAL DEL CURSO DE INTERACCION HUMANO COMPUTADOR UNSA 
   Este proyecto es una mejora del trabajo original de Takeyamayuki "https://github.com/takeyamayuki/NonMouse"
   
</div>

<p align="center">
  <a href="https://github.com/takeyamayuki/NonMouse/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/takeyamayuki/nonmouse" />
  </a>
  <a href="https://github.com/takeyamayuki/NonMouse/releases">
    <img src="https://img.shields.io/github/v/release/takeyamayuki/nonmouse" />
  </a>
  <a href="https://zenn.dev/ninzin/articles/94b05fdb9edf53">
    <img src="https://img.shields.io/badge/Zenn%20Likes-112-blue" />
  </a>  
  <a href ="https://pypi.org/project/nonmouse/">
     <img src="https://static.pepy.tech/personalized-badge/nonmouse?period=total&units=international_system&left_color=grey&right_color=green&left_text=PyPI%20downloads" />
   </a>

  
</p>

--- 

<table>
<tr>
<td><img src="https://user-images.githubusercontent.com/22733958/135473409-9ddf2fc5-4722-4e55-8eef-64476635c10d.gif"></td>
<td><img src="https://user-images.githubusercontent.com/22733958/129838897-86da6861-b3a5-4e14-98fe-400a27c894d7.gif"></td>
</tr>
</table>

# Description 
SkillPointer tiene como objetivo añadir nuevas funcionalidades dirigidas a la creación de una interfaz de estimulacion de motricidad fina habilidades de escritura de niños
# Installation

## 🐍 PyPI
Run the following script. Use python 3.9

```sh
$ git clone 'https://github.com/sarasofiaa/IHCproyect.git'
$ pip install virtualenv
$ virtualenv -p python 
$ pip install nonmouse
$ pip install -r requirements.txt
```
(If you have trouble installing mediapipe, please visit the [official website](https://google.github.io/mediapipe/getting_started/install.html).)


# LEVANTAR
> **Note**  
> The built binary files can be downloaded from latest realease.


In app-mac.spec and app-win.spec, change `pathex` to fit your environment.   
Run the following scripts for each OS.  

- windows

   Copy and paste the location obtained by `pip show mediapipe` into `datas`, referring to what is written originally.  
   Run the following script.
   ```sh
   $ pip show mediapipe
   ...
   Location: c:\users\namik\appdata\local\programs\python\python37\lib\site_packages
   ...
   $ pip show opencv-python
   ...
   Location: c:\users\namik\appdata\local\programs\python\python37\lib\site_packages
   ...
   
   #Copy and paste into the datas in win.spec
   $ pyinstaller config/win.spec
   $ python -m nonmouse #Levantara la interfaz 
   ... ````


   ```
