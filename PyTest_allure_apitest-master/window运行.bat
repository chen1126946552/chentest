@ECHO OFF

ECHO.:::::::::::::::::::::::::::::::::::::::::::::::::
 
ECHO.:: 					       ::

ECHO.::                 �ӿڲ���                    ::

ECHO.:: 					       ::

ECHO.::               ���ߣ� ����                   ::

ECHO.:: 					       ::

ECHO.::               �汾  V1.0.0                  ::

ECHO.:: 					       ::

ECHO.::               ʱ�� 2018.11.10               ::

ECHO.:: 					       ::

ECHO.:::::::::::::::::::::::::::::::::::::::::::::::::

ECHO.[ INFO ] ���л���׼��

REM �������ļ��а�װ����������
if exist requirements.txt pip install -r requirements.txt
if not exist requirements.txt echo requirements.txt does not exist

REM ���нű�
python main.py