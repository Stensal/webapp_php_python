<?php

$ssoTool = new ssoHelper();
if(GITHUB_LOGGED_IN){
    $ret = $ssoTool->auto_login(GITHUB_USER_NAME,GITHUB_USER_EMAIL);
}else{
    //logout
}