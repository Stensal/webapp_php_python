<?php
include_once('../session.php');

define('IN_PHPBB', true);
$phpbb_root_path = './';
$phpEx = substr(strrchr(__FILE__, '.'), 1);
include_once($phpbb_root_path . 'common.' . $phpEx);
include_once($phpbb_root_path . 'includes/functions_user.' . $phpEx);
include_once($phpbb_root_path . 'github-auth-functions.' . $phpEx);


print_r($session->listAll());

// Start session management
$user->session_begin();
$auth->acl($user->data);
$user->setup();


/**
 * @param $user_name
 * @param $user_email
 * @description: if $user_name already exists in phpbb db, it will do login to phpbb,
 * or it will create a new phpbb user and then do login
 */

$user_name = request_var('user_name', '', true);
$user_email = request_var('user_email', '', true);
if(!$user_name || !$user_email)
{
    echo 'Username and email is required!';
    exit();
}

if(!github_user_logged_in())
{

    if(!github_username_exists($user_name))
    {
        // do register
        $password = github_random_password(12);
        $userdata = array(
            'username' => $user_name,
            'user_email' => $user_email,
            'user_password' => $password
        );

        $result = github_register($userdata);

        if($result['status'] !== GITHUB_REGIST_SUCCESS)
        {
            echo "Regist failed! \n";
            print_r($result);
            die();
        }

        echo "Regist successfully! \n";
    }


    // do login
    $result = github_username_login($user_name);

    // result
    if ($result['status'] == LOGIN_SUCCESS)
    {
        //User was successfully logged into phpBB
        echo "User was successfully logged into phpBB \n";
    }
    else
    {
        //User's login failed
        echo "User's login failed. \n";
        print_r($result);
    }
}
else{
    //User is already logged in
    echo "User is already logged in. \n";
}