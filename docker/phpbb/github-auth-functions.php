<?php

define('GITHUB_REGIST_SUCCESS', 1);
define('GITHUB_REGIST_BREAK', 2);

/**
 * @return mixed
 */
function github_user_logged_in(){
    global $user;
    return $user->data['is_registered'];
}

/**
 * @param $username
 * @param bool $autologin
 * @param int $viewonline
 * @param int $admin
 * @return bool
 */
function github_username_login($username, $autologin = false, $viewonline = 1, $admin = 0){
    global $user;

    $login = github_auth_db_login($username);

    if ($login['status'] == LOGIN_SUCCESS)
    {
        $result = $user->session_create($login['user_row']['user_id'], $admin, $autologin, $viewonline);
        if($result === true)
        {
            return array(
                'status'		=> LOGIN_SUCCESS,
                'error_msg'		=> false,
                'user_row'		=> $login['user_row'],
            );
        }
        return array(
            'status'		=> LOGIN_BREAK,
            'error_msg'		=> $result,
            'user_row'		=> $login['user_row']
        );
    }
    return $login;
}


/**
 * @param $userdata
 * @return array
 */
function github_register($userdata){
    global $phpbb_container;

    if(github_username_exists($userdata['username']))
    {
        return array(
            'status' => GITHUB_REGIST_BREAK,
            'error_msg' => 'USERNAME_TAKEN',
            'user_id' => 0
        );
    }
    if(github_email_exists($userdata['user_email']))
    {
        return array(
            'status' => GITHUB_REGIST_BREAK,
            'error_msg' => 'EMAIL_TAKEN',
            'user_id' => 0
        );
    }

    $passwords_manager = $phpbb_container->get('passwords.manager');

    $user_row = array(
        'username'				=> $userdata['username'],
        'user_password'			=> $passwords_manager->hash($userdata['user_password']),
        'user_email'			=> $userdata['user_email'],
        'group_id'				=> 2, //REGISTERED
        'user_timezone'			=> 'Asia/Shanghai',
        'user_lang'				=> 'zh_cmn_hans',
        'user_type'				=> 0, //USER_NORMAL
        'user_actkey'			=> '',
        'user_ip'				=> '0.0.0.0',
        'user_regdate'			=> time(),
        'user_inactive_reason'	=> 0,
        'user_inactive_time'	=> 0,
    );
    $user_row['user_new'] = 1;

    $user_id = user_add($user_row);

    return array(
        'status' => GITHUB_REGIST_SUCCESS,
        'error_msg' => false,
        'user_id' => $user_id
    );
}

/**
 * @param $username
 * @return array
 */
function github_auth_db_login($username){
    global $db;

    $username_clean = utf8_clean_string($username);

    $sql = 'SELECT *
			FROM ' . USERS_TABLE . "
			WHERE username_clean = '" . $db->sql_escape($username_clean) . "'";
    $result = $db->sql_query($sql);
    $row = $db->sql_fetchrow($result);
    $db->sql_freeresult($result);

    if(!$row)
    {
        return array(
            'status'	=> LOGIN_ERROR_USERNAME,
            'error_msg'	=> 'LOGIN_ERROR_USERNAME',
            'user_row'	=> array('user_id' => ANONYMOUS),
        );
    }

    return array(
        'status'		=> LOGIN_SUCCESS,
        'error_msg'		=> false,
        'user_row'		=> $row,
    );
}


/**
 * @param $email
 * @return bool|string
 */
function github_email_exists($email){
    global $config, $db, $user;

    $sql = 'SELECT user_email_hash
			FROM ' . USERS_TABLE . "
			WHERE user_email_hash = " . $db->sql_escape(phpbb_email_hash($email));
    $result = $db->sql_query($sql);
    $row = $db->sql_fetchrow($result);
    $db->sql_freeresult($result);

    if ($row)
    {
        return true;
    }

    return false;
}

/**
 * @param $username
 * @return bool|string
 */
function github_username_exists($username){
    global $config, $db, $user;

    $clean_username = utf8_clean_string($username);

    $sql = 'SELECT username
		FROM ' . USERS_TABLE . "
		WHERE username_clean = '" . $db->sql_escape($clean_username) . "'";
    $result = $db->sql_query($sql);
    $row = $db->sql_fetchrow($result);
    $db->sql_freeresult($result);

    if ($row)
    {
        return true;
    }

    return false;
}


function github_random_password($length) {
    $alphabet = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUWXYZ0123456789";
    $alphabetMax = strlen($alphabet)-1;
    $pass = array();
    for ($i = 0; $i < $length; $i++) {
        $n = rand(0, $alphabetMax);
        $pass[] = $alphabet[$n];
    }
    return implode($pass);
}