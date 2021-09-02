$(".opcion_idioma").on("click", function (e) {
   if (e.currentTarget.id == "idioma_español") {
      $("#selecionar_idioma").val("es-mx");
   }
   else if(e.currentTarget.id == "idioma_ingles"){
      $("#selecionar_idioma").val("en");
   }
   console.log($("#idioma_actual").val())
   if ($("#idioma_actual").val() != $("#selecionar_idioma").val()) {
      $("#idioma_form").submit();
   }
});

function fnInicializarPanel(panel, boton, botonCierre = "") {
   var quickActionsPanel3 = KTUtil.get(panel);
   if (botonCierre == ""){
      botonCierre = "kt_offcanvas_toolbar_quick_actions_close";
   }
   var head = KTUtil.find(quickActionsPanel3, '.kt-offcanvas-panel__head');
   var body = KTUtil.find(quickActionsPanel3, '.kt-offcanvas-panel__body');

   var offcanvas = new KTOffcanvas(quickActionsPanel3, {
      overlay: true,
      baseClass: 'kt-offcanvas-panel',
      closeBy: botonCierre,
      toggleBy: boton
   });

   KTUtil.scrollInit(body, {
      disableForMobile: true,
      resetHeightOnDestroy: true,
      handleWindowResize: true,
      height: function() {
         var height = parseInt(KTUtil.getViewPort().height);

         if (head) {
            height = height - parseInt(KTUtil.actualHeight(head));
            height = height - parseInt(KTUtil.css(head, 'marginBottom'));
         }

         height = height - parseInt(KTUtil.css(quickActionsPanel3, 'paddingTop'));
         height = height - parseInt(KTUtil.css(quickActionsPanel3, 'paddingBottom'));

         return height;
      }
   });
}

if( jQuery.validator != undefined ){
   $.validator.setDefaults({
      errorPlacement: function (
         error,
         elemento
      ) {
         elemento.removeClass("is-valid");
         elemento.addClass("is-invalid");
         if(elemento.is("select")){
            (elemento.data("select2").$selection).removeClass("is-valid");
            (elemento.data("select2").$selection).addClass("is-invalid");
            error.insertAfter(elemento.next()).addClass("error invalid-feedback");
         }else{
            error.insertAfter(elemento).addClass("error invalid-feedback");
         }
      },
      unhighlight: function(
         elemento
      ){
         $(elemento).removeClass("is-invalid").addClass("is-valid");
         if($(elemento).is("select")){
            ($(elemento).data("select2").$selection).removeClass("is-invalid").addClass("is-valid");
         }
      },
   });
}


toastr.options = {
   "closeButton": true,
   "debug": false,
   "newestOnTop": true,
   "progressBar": true,
   "positionClass": "toast-top-right",
   "preventDuplicates": false,
   "showDuration": "300",
   "hideDuration": "1000",
   "timeOut": "5000",
   "extendedTimeOut": "1000",
   "showEasing": "swing",
   "hideEasing": "linear",
   "showMethod": "fadeIn",
   "hideMethod": "fadeOut"
};