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