<?php

class ssoHelper{

    public function random_pwd($length){
        $alphabet = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUWXYZ0123456789";
        $alphabetMax = strlen($alphabet)-1;
        $pass = array();
        for ($i = 0; $i < $length; $i++) {
            $n = rand(0, $alphabetMax);
            $pass[] = $alphabet[$n];
        }
        return implode($pass);
    }

    public function find_user_by_email($email){
        global $db;

        $sql = 'SELECT *
			FROM ' . USERS_TABLE . "
			WHERE user_email_hash = " . $db->sql_escape(phpbb_email_hash($email));
        $result = $db->sql_query($sql);
        $row = $db->sql_fetchrow($result);
        $db->sql_freeresult($result);

        return $row;
    }

    public function find_user_by_name($username){
        global $db;
        $clean_username = utf8_clean_string($username);

        $sql = 'SELECT *
		FROM ' . USERS_TABLE . "
		WHERE username_clean = '" . $db->sql_escape($clean_username) . "'";
        $result = $db->sql_query($sql);
        $row = $db->sql_fetchrow($result);
        $db->sql_freeresult($result);

        return $row;
    }

    public function regist_user($userdata){
        global $phpbb_container;

        if($this->find_user_by_name($userdata['username'])) return false;
        //if($this->find_user_by_email($userdata['user_email'])) return false;

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

        return $user_id;
    }

    public function do_login($user_id){
        global $user;
        $login = $user->session_create($user_id, false, 1, 0);
        return $login;
    }

    public function auto_login($user_name, $user_email){
        global $user;

        if(!$user->data['is_registered']){
            if($row = $this->find_user_by_name($user_name)){
                return $this->do_login($row['user_id']);
            }else{
                $password = $this->random_pwd(12);
                $userdata = array(
                    'username' => $user_name,
                    'user_email' => $user_email,
                    'user_password' => $password
                );
                $user_id = $this->regist_user($userdata);
                return $this->do_login($user_id);
            }
        }else{
            return true;
        }
    }

    public function auto_logout(){
        global $user;
        if($user->data['group_id'] == '5'){ // this is admin user
            return false;
        }
        return $user->session_kill();
    }
}