$(document).ready(function () {
  /* 메뉴 */
  $('.btn_menu').on('click', function () {
    $('.menu_wrap').animate({ left: '0px' });
    $('.footer').fadeOut();
  });
  $('.menu_wrap .btn_close').on('click', function () {
    $('.menu_wrap').animate({ left: '-120%' });
    $('.footer').fadeIn();
  });
  $('.depth1 > li').on('click', function () {
    var idx = $(this).index();
    $('.depth1 > li').removeClass('on');
    $('.depth1 > li').eq(idx).addClass('on');
  });
  /* 뒤로가기 */
  $('.btn_back').on('click', function () {
    window.history.back();
  });
  /* 모달 */
  $('.modal .btn_close').on('click', function () {
    $(this).parents('.modal').fadeOut();
    $('.modal_bg').fadeOut();
    $('.footer').fadeIn();
  });
  /* 고객센터 */
  $('.cs .list li .title').on('click', function () {
    if ($(this).parent().hasClass('on')) {
      $(this).parent().removeClass('on');
    } else {
      $('.list li').removeClass('on');
      $(this).parent().addClass('on');
    }
  });
  /* 탭 */
  $('.tab_button button').on('click', function () {
    var idx = $(this).index();
    $('.tab_button button, .tab_content .item').removeClass('on');
    $('.tab_button button').eq(idx).addClass('on');
    $('.tab_content .item').eq(idx).addClass('on');
  });
});

function modal(modal_name) {
  $('.modal.' + modal_name).fadeIn();
  $('.modal.' + modal_name)
    .next('.modal_bg')
    .fadeIn();
  $('.footer').fadeOut();
}
function copyToClipboard() {
  const copytext = '15.164.45.203,13.209.61.131,13.209.229.133';
  copyStringToClipboard(copytext);
}
function copyStringToClipboard(string) {
  function handler(event) {
    event.clipboardData.setData('text/plain', string);
    event.preventDefault();
    document.removeEventListener('copy', handler, true);
  }
  document.addEventListener('copy', handler, true);
  document.execCommand('copy');
  alert('YBBot 고정 IP가 복사되었습니다.');
}
