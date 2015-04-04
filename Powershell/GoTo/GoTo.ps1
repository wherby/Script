function GoTO([String] $uri){
 #Write-Host $paths.Get_Item($uri)
 $keys=$paths.Keys
 $enum=$keys.GetEnumerator()
 while($enum.MoveNext()){
    if($enum.key.indexof($uri) -eq 0){cd $paths.get_Item($enum.key);break}
 }
}

$paths=@{"python"='C:\Python27\MyTest\Pybook';"home"='C:\Users\Administrator'}

GoTO $args[0]