<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU GPL v3.0 License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/d3finit/chess-engine">
  <!--
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->
<h3 align="center">Chess Engine</h3>

  <p align="center">
    a chess engine made with python, tensorflow, and python-chess
    <br />
    <!--<a href="https://github.com/d3finit/chess-engine"><strong>Explore the docs »</strong></a>
    <br />
    <br />-->
    <a href="https://github.com/d3finit/chess-engine">View Demo</a>
    ·
    <a href="https://github.com/d3finit/chess-engine/issues">Report Bug</a>
    ·
    <a href="https://github.com/d3finit/chess-engine/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* python
* python-chess
* tensorflow

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

What you need to get started
* python3 (tested on 3.11.5)
  ```sh
  python3 --version
  ```

### Installation

1. Clone the repo.
   ```sh
   git clone https://github.com/d3finit/chess-engine.git
   ```
2. Navigate to the repository folder.
   ```sh
   cd Chess-Engine
   ```
3. Install the required libraries
   ```sh
   pip install -r requirements.txt
   ```
   Depending on your configuration the command
   ```sh
   python3 -m pip install -r requirements.txt
   ```
   may be necessary to install the libraries.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use 
```sh
python3 main.py -matesd <number> -materialsd <number> [-sf]
```
to start the engine.

_For more examples, please refer to the [Documentation](https://github.com/d3finit/Chess-Engine/wiki)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Increase the model size
- [ ] Optimize the code
- [ ] Make GitHub wiki
  - [ ] Usage
  - [ ] Document how the code works
- [ ] Add SAN parsing

See the [open issues](https://github.com/d3finit/chess-engine/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU GPL v3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/d3finit/chess-engine](https://github.com/d3finit/chess-engine)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS 
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/d3finit/chess-engine.svg?style=for-the-badge
[contributors-url]: https://github.com/d3finit/chess-engine/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/d3finit/chess-engine.svg?style=for-the-badge
[forks-url]: https://github.com/d3finit/chess-engine/network/members
[stars-shield]: https://img.shields.io/github/stars/d3finit/chess-engine.svg?style=for-the-badge
[stars-url]: https://github.com/d3finit/chess-engine/stargazers
[issues-shield]: https://img.shields.io/github/issues/d3finit/chess-engine.svg?style=for-the-badge
[issues-url]: https://github.com/d3finit/chess-engine/issues
[license-shield]: https://img.shields.io/github/license/d3finit/chess-engine.svg?style=for-the-badge
[license-url]: https://github.com/d3finit/chess-engine/blob/master/LICENSE.txt