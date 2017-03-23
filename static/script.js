var page_width=document.body.clientWidth;
var bg_img_top=490;
var logo_top=130;
var letter_1_top=392;
var letter_2_left=388;
var letter_2_top=145;
var letter_3_left=207;
var letter_3_top=156;
var number_top=230;
var number_left=340;
var number_height=30;
var phone_top=300;
var phone_left=340;
var phone_height=30;
var icon_left=665;
var icon_top=145;
var index,state,width;

/////////////////寬度超過1024時/////////////////
if(page_width>1024){
  /////////////////左距調整/////////////////
  function left_1024(l,w,id){
    var tem=l+w/2+"px";
    $(id).css("left",tem);
  }

  width=page_width-1024;
  left_1024(0,width,"#bg_img");
  left_1024(letter_2_left,width,"#letter_2");
  left_1024(letter_3_left,width,"#letter_3");
  left_1024(icon_left,width,"#icon");
  left_1024(number_left,width,"#number");
  left_1024(phone_left,width,"#phone");
}

/////////////////寬度小於1024時/////////////////
if(page_width<1024){
  /////////////////總長度調整/////////////////  
  index=576*page_width/1024;
  state=index;
  index+="px";
  $("#header_index").css("height",index);
  $("#section_about").css("height",index);
  $("#section_login").css("height",index);

  /////////////////上距調整/////////////////
  function s_1024(num,state,id,Pattern){
    var tem=num*state/576+"px";
    $(id).css(Pattern,tem);
  }

  s_1024(logo_top,state,"#logo","top");
  s_1024(letter_1_top,state,"#letter_1","top");
  s_1024(letter_2_top,state,"#letter_2","top");
  s_1024(letter_3_top,state,"#letter_3","top");
  s_1024(icon_top,state,"#icon","top");
  s_1024(bg_img_top,state,"#bg_img","top");
  s_1024(number_top,state,"#number","top");
  s_1024(phone_top,state,"#phone","top");

  /////////////////左距調整/////////////////
  s_1024(letter_2_left,state,"#letter_2","left");
  s_1024(letter_3_left,state,"#letter_3","left");
  s_1024(icon_left,state,"#icon","left");
  s_1024(number_left,state,"#number","left");
  s_1024(phone_left,state,"#phone","left");

  /////////////////調整輸入方塊寬度/////////////////
  s_1024(number_height,state,"#number","height");
  s_1024(phone_height,state,"#phone","height");
}
