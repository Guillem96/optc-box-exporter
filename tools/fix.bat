REM apply the fix on each photo (.png)

cd data\Portrait

for %%i in (*.png) do magick identify %%i
for %%i in (*.png) do magick convert %%i -strip %%i
for %%i in (*.png) do magick identify %%i

REM end script
echo finish..
set /P user_input=Press any key to terminate...