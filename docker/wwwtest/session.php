<?php
include_once(__DIR__.'/cppcms.php');
$pool = CppCMS_SessionPool::from_config(__DIR__.'/config.js');
$session = $pool->session();
$session->load();

function session_list_all(){
    global $session;
    $list = array();
    $keys = $session->keys();
    foreach($keys as $key){
        $list[$key] = $session[$key];
    }
    return $list;
}