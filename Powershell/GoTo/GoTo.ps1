function GoTo([String] $uri){
 #Write-Host $paths.Get_Item($uri)
 $keys=$paths.Keys
 $enum=$keys.GetEnumerator()
 while($enum.MoveNext()){
    if($enum.key.indexof($uri) -eq 0)
    {
        if($paths.get_Item($enum.key).indexof(";") -gt 0)
        {
            #Write-Host "multi commands"
            $val=$paths.get_Item($enum.key).split(";")
            cd $val[0]
            Invoke-Expression $val[1]
        }
        else
        {
            #Write-Host $enum.key
            #Write-Host "cd"
            cd $paths.get_Item($enum.key);break
        }
    }
 }
}

$paths=@{"python"='C:\Python27';"home"='C:\Users\zhoust';
           }

#GoTo $args[0]
