<?php
function get($key, $default=NULL) {
    return array_key_exists($key, $_GET) ? $_GET[$key] : $default;
}

class githubAuth{
    protected $authorizeURL = 'https://github.com/login/oauth/authorize';
    protected $tokenURL = 'https://github.com/login/oauth/access_token';
    protected $apiURLBase = 'https://api.github.com/';
    protected $homeUri = 'http://localhost:8000/auth.php';
    protected $redirectUri = 'http://localhost:8000/auth.php?callback';

    public function __construct(){
        if(defined('HOME_URI')){
            $this->homeUri = HOME_URI;
        }
        if(defined('REDIRECT_URI')){
            $this->redirectUri = REDIRECT_URI;
        }

        if(get('act') == 'logout'){
            $this->authLogout();
            header('Location: ' . $this->homeUri);
            die();

        } else if(get('act') == 'login'){
            $this->authLogin();
        } else if(isset($_GET['callback'])){
            $this->authCallback();
        }
    }

    public function authLogin(){
        global $session;

        $state = hash('sha256', microtime(TRUE).rand().$_SERVER['REMOTE_ADDR']);
        $session['state'] = $state;

        unset($session['access_token']);

        $session->save();

        $params = array(
            'client_id' => OAUTH2_CLIENT_ID,
            'redirect_uri' => $this->redirectUri,
            'scope' => 'user',
            'state' => $state
        );

        // Redirect the user to Github's authorization page
        header('Location: ' . $this->authorizeURL . '?' . http_build_query($params));
        die();
    }

    public function authLogout(){
        global $session;

        unset($session['access_token']);
        $session->save();
    }

    public function authCallback(){
        global $session;

        // Verify the state matches our stored state
        if(!get('state') || $session['state'] != get('state')) {
            header('Location: ' . $this->homeUri);
            die();
        }

        // Exchange the auth code for a token
        $token = $this->apiRequest($this->tokenURL, array(
            'client_id' => OAUTH2_CLIENT_ID,
            'client_secret' => OAUTH2_CLIENT_SECRET,
            'redirect_uri' => $this->redirectUri,
            'state' => get('state'),
            'code' => get('code')
        ));

        $session['access_token'] = $token->access_token;

        $user = $this->userInfo();
        $session['github_user_name'] = $user->login;
        $session['github_user_email'] = $user->email;
        $session->save();

        header('Location: ' . $this->homeUri);
    }

    function apiRequest($url, $post=FALSE, $headers=array()) {
        global $session;

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
        curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)");

        if($post)
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));

        $headers[] = 'Accept: application/json';

        if(isset($session['access_token']))
            $headers[] = 'Authorization: Bearer ' . $session['access_token'];

        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

        $response = curl_exec($ch);

        return json_decode($response);
    }


    function loggedIn(){
        global $session;
        if($session['access_token']){
            return true;
        }
        return false;
    }

    function userInfo(){
        return $this->apiRequest($this->apiURLBase . 'user');
    }
}