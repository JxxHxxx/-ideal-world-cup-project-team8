function logout(){
        $.removeCookie('mytoken', { path: '/' });
        alert('로그아웃!');
        window.location.href='/';
  }