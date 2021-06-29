html_data = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
  rel="stylesheet"
  integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
  crossorigin="anonymous"
/>
<style type="text/css">
  body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 1em;
  }

  a {
    text-decoration: none;
    color: #2152b9;
  }
  .starry-background-wrapper {
    background-image: linear-gradient(
        to bottom,
        rgba(0, 0, 0, 0.2),
        rgba(0, 0, 0, 0.5)
      ),
      url("/styles/img/background.jpg");
    margin: 0 -15px;
    background-attachment: fixed;
  }

  .logo-header {
    padding: 50px;
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    -webkit-font-smoothing: antialiased;
    font-weight: 300;
    background-attachment: fixed;
    text-align: center;
  }

  .logo-link {
    color: #fff;
    text-decoration: none;
  }

  .logo-header img {
    max-width: 75px;
    position: relative;
    top: -5px;
    max-height: 66px;
  }

  .logo-header a,
  .logo-header a:hover,
  .logo-header a:visited {
    color: #fff;
    text-decoration: none;
  }

  .main-container {
    margin-top: 40px;
    margin-bottom: 40px;
  }

  .title {
    font-weight: bold;
  }

  .main-container a {
    line-height: 1.2;
    letter-spacing: 0.01em;
    word-spacing: 0.05em;
  }

  @media screen and (min-width: 480px) {
    .logo-header {
      font-size: 22px;
    }
  }
  @media screen and (min-width: 788px) {
    .logo-header {
      font-size: 40px;
    }
  }

  .footer_wrapper {
    background-color: #484f4f;
    color: white;
    font-size: 1.1em;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-weight: 300;
    padding: 30px 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .footer_wrapper > * {
    padding: 0 30px;
  }

  .footer_wrapper .footer_brand_extra {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.7em;
    max-width: 300px;
  }

  @media (min-width: 788px) {
    .footer_wrapper .footer_brand_extra {
      width: 100%;
    }
  }

  .footer_wrapper .footer_brand_logos #nasa-logo {
    width: 80px;
  }

  .footer_wrapper .footer_brand_logos #smithsonian-logo {
    width: 66px;
  }

  .footer_wrapper .footer_brand_logos #cfa-logo {
    width: 100px;
    padding-left: 5px;
  }

  @media (min-width: 788px) {
    .footer_wrapper {
      flex-direction: row;
    }
  }

  .footer_links {
    list-style: none;
    padding-left: 0;
    margin-top: 0;
    margin-bottom: 0;
  }

  .footer_links a {
    text-decoration: none;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 100;
  }

  .footer_links a:hover {
    color: #5683e0;
  }

  .footer_links li {
    line-height: 1.25;
    margin-bottom: 8px;
  }

  .footer_list_title {
    font-weight: 400;
    margin-bottom: 1em;
  }

  .s-footer {
    width: 100%;
  }
</style>
<script
  src="https://kit.fontawesome.com/6b7af20fb7.js"
  crossorigin="anonymous"
></script>
    <title>NASA/ADS Search</title>
</head>
<body>
    
    <div class="header-container">
        <header class="starry-background-wrapper">
    <div class="logo-header">
        <a href="/">
            <img src="/styles/img/transparent_logo.svg" alt="The Astrophysics Data System Logo">
            <b>astrophysics</b>&nbsp;data system
        </a>
    </div>
</header>
    </div>

    <div class="main-container container-sm">
        
        <h3 class="text-center"> links for <a href=/abs/1987gady.book.....B/abstract><b>1987gady.book.....B</b></a></h3>
        <div class="list-group">
            
                <div class="list-group-item">
                    <a href="http://arxiv.org/abs/1307.6556" class="title">
                        http://arxiv.org/abs/1307.6556
                    </a>
                    
                </div>
            
                <div class="list-group-item">
                    <a href="http://arxiv.org/pdf/1307.6556" class="title">
                        http://arxiv.org/pdf/1307.6556
                    </a>
                    
                </div>
            
                <div class="list-group-item">
                    <a href="http://dx.doi.org/10.1093%2Fmnras%2Fstt1379" class="title">
                        http://dx.doi.org/10.1093%2Fmnras%2Fstt1379
                    </a>
                    
                </div>
            
                <div class="list-group-item">
                    <a href="http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf" class="title">
                        http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf
                    </a>
                    
                </div>
            
        </div>
        
    </div>

    <div class="footer-container">
        <footer>
  <div class="footer_wrapper">
    <div class="footer_brand">
      &copy; The SAO/NASA Astrophysics Data System
      <div class="footer_brand_extra">
        <p>
          <i class="fa fa-envelope" aria-hidden="true"></i>
          adshelp[at]cfa.harvard.edu
        </p>
        <p>
          The ADS is operated by the Smithsonian Astrophysical Observatory under
          NASA Cooperative Agreement <em>80NSSC21M0056</em>
        </p>
      </div>
      <div class="footer_brand_logos">
        <a href="http://www.nasa.gov" target="_blank" rel="noreferrer noopener">
          <img src="/styles/img/nasa.svg" alt="NASA logo" id="nasa-logo" />
        </a>
        <a href="http://www.si.edu" target="_blank" rel="noreferrer noopener">
          <img
            id="smithsonian-logo"
            src="/styles/img/smithsonian.svg"
            alt="Smithsonian logo"
          />
        </a>
        <a
          href="https://www.cfa.harvard.edu/"
          target="_blank"
          rel="noreferrer noopener"
        >
          <img
            src="/styles/img/cfa.png"
            alt="Harvard Center for Astrophysics logo"
            id="cfa-logo"
          />
        </a>
      </div>
    </div>
    <div class="footer_list">
      <div class="footer_list_title">
        Resources
      </div>
      <ul class="footer_links">
        <li>
          <a href="/about/" target="_blank" rel="noreferrer noopener">
            <i class="fa fa-question-circle" aria-hidden="true"></i> About ADS
          </a>
        </li>
        <li>
          <a href="/help/" target="_blank" rel="noreferrer noopener">
            <i class="fa fa-info-circle" aria-hidden="true"></i> ADS Help
          </a>
        </li>
        <li>
          <a href="/help/whats_new/" target="_blank" rel="noreferrer noopener">
            <i class="fa fa-bullhorn" aria-hidden="true"></i> What's New
          </a>
        </li>
        <li>
          <a href="/about/careers/" target="_blank" rel="noreferrer noopener">
            <i class="fa fa-group" aria-hidden="true"></i> Careers@ADS
          </a>
        </li>
        <li>
          <a
            href="/help/accessibility/"
            target="_blank"
            rel="noreferrer noopener"
          >
            <i class="fa fa-universal-access" aria-hidden="true"></i>
            Accessibility
          </a>
        </li>
      </ul>
    </div>
    <div class="footer_list">
      <div class="footer_list_title">
        Social
      </div>
      <ul class="footer_links">
        <li>
          <a
            href="//twitter.com/adsabs"
            target="_blank"
            rel="noreferrer noopener"
          >
            <i class="fa fa-twitter" aria-hidden="true"></i> @adsabs
          </a>
        </li>
        <li>
          <a href="/blog/" target="_blank" rel="noreferrer noopener">
            <i class="fa fa-newspaper-o" aria-hidden="true"></i> ADS Blog
          </a>
        </li>
      </ul>
    </div>
    <div class="footer_list">
      <div class="footer_list_title">
        Project
      </div>
      <ul class="footer_links">
        <li>
          <a href="/core">Switch to basic HTML</a>
        </li>
        <li>
          <a href="/help/privacy/" target="_blank" rel="noreferrer noopener"
            >Privacy Policy</a
          >
        </li>
        <li>
          <a href="/help/terms" target="_blank" rel="noreferrer noopener"
            >Terms of Use</a
          >
        </li>
        <li>
          <a
            href="http://www.cfa.harvard.edu/sao"
            target="_blank"
            rel="noreferrer noopener"
            >Smithsonian Astrophysical Observatory</a
          >
        </li>
        <li>
          <a href="http://www.si.edu" target="_blank" rel="noreferrer noopener"
            >Smithsonian Institution</a
          >
        </li>
        <li>
          <a
            href="http://www.nasa.gov"
            target="_blank"
            rel="noreferrer noopener"
            >NASA</a
          >
        </li>
      </ul>
    </div>
  </div>
</footer>
    </div>

</body>
</html>'''