$(document).ready(function() {

   //Efecto Menu de Navegación
   posicionarMenu();

   $(window).scroll(function() {
    	posicionarMenu();
   });

   function posicionarMenu() {
      if ($(window).scrollTop() >= 100){
         $('.menu-pleca').addClass("menu-scroll");
      } else {
         $('.menu-pleca').removeClass("menu-scroll");
      }
   }

   fnFiltros();
   $(window).resize( fnFiltros );

   //Funciones del menu movil
   $(".boton-menu-sm").click(function(){
      $(".menu-sm").addClass("abierto");
      $("body").addClass("no-scroll");
      $(".overlay").fadeIn(500);
   });

   $(".boton-cerrar-menu-sm").click(function(){
      $(".menu-sm").removeClass("abierto");
      $("body").removeClass("no-scroll");
      $(".overlay").fadeOut(500);
   });

   $(".overlay").click(function(){
      $(".menu-sm").removeClass("abierto");
      $("body").removeClass("no-scroll");
      $(".overlay").fadeOut(500);
   });

   // Boton Ir hacia Arriba
   $(window).scroll(function(){
      if ($(this).scrollTop() > 500) {
         $('.scrollup').addClass("show-scrollup");
      } else {
         $('.scrollup').removeClass("show-scrollup");
      }
   });

   $('.scrollup').click(function(){
      $("html, body").animate({ scrollTop: 0 }, 600);
      return false;
   });

});

function fnFiltros() {
   if ($(window).width() < 992){
      if( !$('#filtros-busqueda').hasClass("click") ){
         $('#filtros-busqueda').removeClass("show");
      }
   } else {
      $('#filtros-busqueda').addClass("show");
   }
}

function fnShowFiltros() {
   if( !$('#filtros-busqueda').hasClass("click") ){
      $('#filtros-busqueda').addClass("click");
   }else{
      $('#filtros-busqueda').removeClass("click");
   }
}