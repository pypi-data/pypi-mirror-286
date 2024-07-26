Stacksim
========

Stacksim is a python package for simulating/visualizing stack operations. It also provides a sphinx extension for generating stack diagrams



CLI 
---


To run the cli, 

.. code::

    stacksim 

This will start the cli interface. 

.. code: bash 

    (stacksim)>>  push <base ptr>
    (stacksim)>>  push varg2: 0x0042  --note varg2 for printf
    (stacksim)>>  push varg1: 0x0041  --note varg1 for printf
    (stacksim)>>  push <format string> --size 16   --note format string for printf
    (stacksim)>>  push <ret to main>




.. code::

                    ┌────────────────────────────────────────────────┐
           0x7ffffc8│x                                               │
                    ├────────────────────────────────────────────────┤
           0x7ffffc9│y                                               │
                    ├───────────────────────z────────────────────────┤
           0x7ffffca│                                                │ <-- dead stack space
                    └────────────────────────────────────────────────┘
                    ╭─vuln───────────────────────────────────────────╮
                    ├──────────────────buffer [16]───────────────────┤
           0x7ffffcb│                                                │
                    :                                                :
                    ├──────────────────────ret───────────────────────┤
           0x7ffffdb│<0x00ffff6799>                                  │ <-- return to main
                    ╰────────────────────────────────────────────────╯
                    ╭─main───────────────────────────────────────────╮
                    ├───────────────────────i────────────────────────┤
           0x7ffffdc│20                                              │
                    ├──────────────────buffer [16]───────────────────┤
           0x7ffffdd│                                                │
                    :                                                :
                    ├──────────────────────arg1──────────────────────┤
           0x7ffffed│1                                               │
                    ├──────────────────────arg2──────────────────────┤
           0x7ffffee│45                                              │
                    ╰────────────────────────────────────────────────╯
                    ┌────────────────────etc [16]────────────────────┐
           0x7ffffef│                                                │ <-- whatever happend before main?
                    :                                                :
                    └────────────────────────────────────────────────┘
           0x7ffffff───────────────── End Of Stack ─────────────────