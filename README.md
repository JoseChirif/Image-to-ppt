<h1> <img src="https://raw.githubusercontent.com/JoseChirif/Pictures-to-slides/refs/heads/main/assets/Icon.png" width="20" height="20" loading="lazy"/>  PICTURES TO SLIDES </h1>


Easily insert all images from a folder into PowerPoint slides with pre-set formats in just a few clicks!

![PICTURES TO SLIDES POWER POINT](https://github.com/user-attachments/assets/aa764d28-585c-4801-ba17-d073a37ad88d)

  <!--- Badges /> --->
<p align="center">
  <img src="https://img.shields.io/github/languages/top/JOSECHIRIF/Pictures-to-slides" alt="Languages" loading="lazy"/>
  &nbsp;
  <img src="https://img.shields.io/badge/python-3.11.5-blue" alt="Python version" loading="lazy"/>
  &nbsp;
  <img src="https://img.shields.io/github/license/JoseChirif/Pictures-to-slides" alt="License" loading="lazy"/>
  &nbsp;
  <img src="https://img.shields.io/github/release/JoseChirif/Pictures-to-slides" alt="release" loading="lazy"/>
</p>

<br>

# Table of contents
- [Video instructions](#%EF%B8%8F-video-instructions)
- [Setup](#%EF%B8%8F-setup)
- [Instructions](#-instructions)
- [Documentation and colaboration](#%EF%B8%8F-documentation-and-collaboration)
- [Thanks](#thanks-)
- [Author](#%EF%B8%8F-author)
<br><br>


# ▶️ Video instructions

Check the instruction guide on YouTube 🎬:
- **[English](https://youtu.be/fTE2EfRAfTg?si=bnRbCFJ0ntkQu9C5&t=16)**.
- **[Español](https://youtu.be/3NZgiZd9smI?si=KF_a75XKvC1Arf31&t=19)**. 

<br>
It covers the **📑 execution**, which can be found below in this README.
<br><br>



# 🛠️ SETUP

### 1. Download

<!-- Option a: Download the last release -->
<details>
  <summary>
    Option a: Download the last release
  </summary>
  <br>

  <ol>
    <li>Download the last release.rar
      <table>
        <tr>
        <td><img src="https://github.com/user-attachments/assets/5324536e-40a4-4b8b-9e0c-1d6d4b2df7f2" loading="lazy"/></td>
        <td><img src="https://github.com/user-attachments/assets/4944850f-5813-4b2b-8070-185721ad348d" loading="lazy"/></td>
        </tr>
      </table>
    </li>
    <li>Extract the .rar program
    </li>
  </ol>

</details>
<br>
<!-- Option a: Download the last release:END -->


<!-- Option b: Clone the repository -->
<details>
  <summary>
    Option b: Clone the repository
  </summary>
  <br>

  <ol>
    <li>Clone the repository with the command: <pre><code>git clone https://github.com/JoseChirif/Pictures-to-slides.git </code></pre>
    </li>

  </ol>

</details>
<br>
<!-- Option b: Clone the repository:END -->





### 2. Install requirements

<ol>
 <li> Install virtual environment with command <pre><code>python -m venv venv</code></pre> </li>

<li> Activate the virtual environment:
  <ol> On <strong>Windows</strong>
  <pre><code>venv\Scripts\activate</code></pre></ol> 
  <ol> On <strong>Mac/Linux</strong>
  <pre><code>source venv/bin/activate</code></pre></ol> 
</li>

<li> Install dependencies from requirements.txt: <pre><code>pip install -r requirements.txt</code></pre>  (check that your venv is active). </li>

</ol>
<br>



### 3. Execute
  
<!-- Option a: Make a onefile.exe file - RECOMMENDED (Click here):START -->
<details>
  <summary>
    Option a: Make a onefile.exe file - RECOMMENDED (Click here)
  </summary>
  <br>

  <ol>
    <li>Run: <pre><code>python build_exe.py</code></pre>
      or Run: <pre><code>pyinstaller --onefile --windowed --clean --noupx `
    --add-data "assets/*;assets" `
    --add-data "config/*;config" `
    --add-data "functions/*;functions" `
    --add-data "src/*;src" `
    --add-data "LICENSE;." `
    --add-data "README.md;." `
    --add-data "assets/example pictures/Presentation - Pictures center ppt.jpg;assets/example pictures" `
    --add-data "assets/example pictures/Presentation - pictures covering panoramic slides.jpg;assets/example pictures" `
    --add-data "assets/example pictures/Presentation - pictures in panoramic slides.jpg;assets/example pictures" `
    --hidden-import pptx `
    --hidden-import pptx.oxml `
    --hidden-import pptx.oxml.nsmap `
    --hidden-import pptx.enum `
    --icon "assets/icon.ico" `
    --name "Pictures to slides.exe" `
    "run.py"
</code></pre>
    </li><br>

  <li>Then a "dist" folder will be created in the project's directory, containing a .exe file.
    <img src="https://github.com/user-attachments/assets/f4c9db5c-5dea-4e38-8097-3fbe1834eb85" alt="dist folder" loading="lazy">
  </li>

  </ol>

</details>
<br>
<!-- Option a: Make a onefile.exe file - RECOMMENDED (Click here):END -->



<!-- Option b: Make a .exe file with dependencies (Click here):START -->
<details>
  <summary>
    Option b: Make a .exe file with dependencies (Click here)
  </summary>
  <br>

  <ol>
    <li>Run: <pre><code>pyinstaller --windowed --clean --noupx `
    --add-data "assets/*;assets" `
    --add-data "config/*;config" `
    --add-data "functions/*;functions" `
    --add-data "src/*;src" `
    --add-data "LICENSE;." `
    --add-data "README.md;." `
    --add-data "assets/example pictures/Presentation - Pictures center ppt.jpg;assets/example pictures" `
    --add-data "assets/example pictures/Presentation - pictures covering panoramic slides.jpg;assets/example pictures" `
    --add-data "assets/example pictures/Presentation - pictures in panoramic slides.jpg;assets/example pictures" `
    --hidden-import pptx `
    --hidden-import pptx.oxml `
    --hidden-import pptx.oxml.nsmap `
    --hidden-import pptx.enum `
    --icon "assets/icon.ico" `
    --name "Pictures to slides.exe" `
    "run.py"
</code></pre>
    </li><br>

  <li>Then the folder "dist" will be created in the project's folder. Inside is the .exe file with the folder "_internal".
    <img src="https://github.com/user-attachments/assets/9408a21f-82d5-482b-9a5d-8ed94f1c3cf3" alt="dist folder with dependecies" loading="lazy">
  </li>
  <li>Move and keep .exe file with the folder "_internal" together all the time. <strong>The .exe file won't work if the "_internal" folder is not in the same directory.</strong></li>

  </ol>

</details>
<br>
<!-- Option b: Make a .exe file with dependencies (Click here):END -->




<!-- Option c: Execute from python (Click here):START -->
<details>
  <summary>
    Option c: Execute from python (Click here)
  </summary>
  <br>

  <ol>
    <li>Execute run.py to enter the main menu: 
      <pre><code>python run.py</code></pre>
    </li><br>
    <li><p><strong>Scripts will modify the name of files in project's parent directory instead of where the executable is.</strong></p></li>
    <img src="https://github.com/user-attachments/assets/4f3428f1-864e-478a-914b-5cf54a4f967d" alt="father's directory" loading="lazy">

  </ol>
  

    
</details>
<br>
<!-- Option c: Execute from python (Click here):END -->    



# 📑 INSTRUCTIONS
  1. Move the executable to the folder where the pictures you want to add in slides are located.
    ![move_to_folder](https://github.com/user-attachments/assets/af777011-9422-428b-8372-bdee6a9dd431)
    **If you created the folder "_internal", move them together.**

  2. Run the program.
    ![Main menu](https://github.com/user-attachments/assets/7ff7efb0-7375-4b92-a680-680e5457ac73)

  3. Select any option and a ppt presentation will be added in the same folder.
    ![presentation created](https://github.com/user-attachments/assets/54795205-a965-4fb4-8b6c-1fbbf105eb48)


**WELL DONE, pictures has been added successfully!**


# 🗃️ Documentation and collaboration
**📚 For detailed documentation and collaboration guidelines, please visit the [Wiki!](https://github.com/JoseChirif/Pictures-to-slides/wiki) <br>**
The [Wiki](https://github.com/JoseChirif/Pictures-to-slides/wiki) contains everything you need to get started and contribute effectively. Your support and collaboration are greatly appreciated! 🚀✨

# Thanks! 👏
📸 Thanks to [Andre Furtado](https://www.pexels.com/es-es/@andre-furtado-43594/?filter=photos&sort_by=popularity) for the amazing photo from [Pexels](https://www.pexels.com/es-es/foto/fotografia-de-mujer-rodeada-de-girasoles-1263986/), which I used as an example in the main menu.

✨ Thank you for checking out this project! If you found it useful, feel free to leave a ⭐ on the repository.

<br>

# ✍️ Author
[@Jose Chirif](https://github.com/JoseChirif)

## 🚀 About me
I'm an Industrial Engineer specialized in process optimization, business intelligence, and Applied Artificial Intelligence. I focus on developing AI-driven solutions and data science tools to automate complex analytical workflows and enhance decision-making.

[Porfolio - Network - Contact](https://linktr.ee/jchirif)

<br>

### ❤️ Support me
If you enjoy my work and want to support me, feel free to donate through the links below. Your support means a lot!

<p align="center">
    <a href="https://buymeacoffee.com/Jchirif" target="_blank">
        <img alt="Buy Me a Tea" src="https://img.shields.io/badge/Buy%20Me%20a%20Tea-☕-586DE0?style=for-the-badge&labelColor=586DE0">
    </a>
    &nbsp;    &nbsp;  &nbsp;  
    <a href="https://paypal.me/JChirif" target="_blank">
        <img alt="Paypal" src="https://img.shields.io/badge/Donate%20via%20PayPal-❤️-FF9900?style=for-the-badge&logo=paypal&labelColor=FF9900">
    </a>
</p>
