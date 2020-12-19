# simple-falcon-tutorial

## Introduction
Document: <a href="https://falcon.readthedocs.io/en/stable/user/intro.html">Falcon docs</a>

- <b>Features</b>
    - Fast
      - Falcon turns around requests several times faster than most other Python frameworks.
      - For an extra speed boost, Falcon compiles itself with Cython when available.
      - Also works well with PyPy.
        
    - Reliable
      - The code is rigorously tested with numerous inputs and we require 100% coverage at all times.
      - Falcon does not depend on any external Python packages.
      
    - Flexible
      - Due to Falcon’s minimalist design, Python community members are free to independently innovate on <a href="https://github.com/falconry/falcon/wiki">Falcon add-ons and complementary packages.</a>
      
    - Debuggable
      - It’s easy to tell which inputs lead to which outputs.
      - Automatic request body parsing, are well-documented and disabled by default.
    
    - Supports Python 2.7, 3.5+
    
### Notes
- <b>WSGI</b>
  - <a href="https://paphopu.tistory.com/entry/WSGI%EC%97%90-%EB%8C%80%ED%95%9C-%EC%84%A4%EB%AA%85-WSGI%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80#:~:text=Gunicorn%EC%9D%80%20Python%20WSGI%20HTTP%20Server%EC%9D%B4%EB%8B%A4.&text=Gunicorn%EC%9D%80%20localhost%208000%EB%B2%88,%EA%B0%99%EC%9D%80%20%EC%9E%A5%EC%A0%90%EC%9D%84%20%ED%8F%AC%ED%95%A8%ED%95%9C%EB%8B%A4.">what is WSGI?</a>
  - Bjoern 
  - uWSGI
  - mod_wsgi
  - CherryPy
  - <b>Gunicorn</b>