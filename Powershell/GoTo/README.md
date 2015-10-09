The GoTo file put to home dirctoty

After configure path, then goto the path



From PowerShell, evaluate the variable:

$profile

Verify that the directory specified in $profile exists, create the file if necessary (note: The directory and file are created by the user. Until you do so the first time neither the directory nor file will exist). Edit file specified by $profile in your favorite text editor. At the end of the profile add the line:

```
import-module <path for GoTO.ps1>
```
If you use custom nouns/verbs and you want to avoid the noisy warnings just add the flag "-DisableNameChecking" to your import module call.
```
import-module <path for GoTO.ps1> -DisableNameChecking
```

After that you could using g to invoke command of setting to do any thing.

```
PS C:\Users\zhoust> g p
PS C:\Users\zhoust\Documents\GitHub\Platform-SDK-Portal> g s
PS C:\Users\zhoust\Documents\GitHub\Platform-SDK-JS> g r
PS D:\Coursera\Ruby\RubyOnRails>
```

