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
        session_start();

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
        $_SESSION['state'] = hash('sha256', microtime(TRUE).rand().$_SERVER['REMOTE_ADDR']);

        unset($_SESSION['access_token']);

        $params = array(
            'client_id' => OAUTH2_CLIENT_ID,
            'redirect_uri' => $this->redirectUri,
            'scope' => 'user',
            'state' => $_SESSION['state']
        );

        // Redirect the user to Github's authorization page
        header('Location: ' . $this->authorizeURL . '?' . http_build_query($params));
        die();
    }

    public function authLogout(){
        unset($_SESSION['access_token']);
    }

    public function authCallback(){
        // Verify the state matches our stored state
        if(!get('state') || $_SESSION['state'] != get('state')) {
            header('Location: ' . $this->homeUri);
            die();
        }

        // Exchange the auth code for a token
        $token = $this->apiRequest($this->tokenURL, array(
            'client_id' => OAUTH2_CLIENT_ID,
            'client_secret' => OAUTH2_CLIENT_SECRET,
            'redirect_uri' => $this->redirectUri,
            'state' => $_SESSION['state'],
            'code' => get('code')
        ));
        $_SESSION['access_token'] = $token->access_token;

        header('Location: ' . $this->homeUri);
    }

    function apiRequest($url, $post=FALSE, $headers=array()) {
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
        curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)");

        if($post)
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));

        $headers[] = 'Accept: application/json';

        if($this->session('access_token'))
            $headers[] = 'Authorization: Bearer ' . $this->session('access_token');

        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

        $response = curl_exec($ch);

        return json_decode($response);
    }

    function session($key, $default=NULL) {
        return array_key_exists($key, $_SESSION) ? $_SESSION[$key] : $default;
    }

    function loggedIn(){
        if($this->session('access_token')){
            return true;
        }
        return false;
    }

    function userInfo(){
        return $this->apiRequest($this->apiURLBase . 'user');
    }
}