$(document).ready(function () {
   // Se agregan los siguientes componentes al documento:
   $("#navegador").load('/static/navegador.html');

   function mostrarPwd(contenedor_pwd) {
      if ($(contenedor_pwd + ' input').attr("type") == "text") {
         $(contenedor_pwd + ' input').attr('type', 'password');
         $(contenedor_pwd + ' a i').addClass("glyphicon-eye-open");
         $(contenedor_pwd + ' a i').removeClass("glyphicon-eye-close")
      } else if ($(contenedor_pwd + '  input').attr("type") == "password") {
         $(contenedor_pwd + ' input').attr('type', 'text');
         $(contenedor_pwd + ' a i').addClass("glyphicon-eye-close");
         $(contenedor_pwd + ' a i').removeClass("glyphicon-eye-open")
      }
   }

   var validaForm=function (form){
      var a = $("input[type=text], input[type=password], textarea").serializeArray();
      var r = 0;
      a.forEach(function (el, i, ar) {
         if (el.value === '') {
            $("#form-"+form+" #div-" + el.name).addClass("has-error has-feedback");
            $("#form_error").addClass("alert alert-danger alert-dismissible fade in");
            $("#form-"+form+" #form_error").css("display", "block");
            $("#form-"+form+" #form_error").text('No se llenaron todos los datos.');
            r=1;
         } else {
            $("#form-"+form+" #div-" + el.name).removeClass("has-error has-feedback");
         }
      });
      if (r==0) {
         $("#form-"+form+" #form_error").css("display", "none");
         $("#form-"+form+" #form_error").text("");
      }
      return $("#form-"+form+" #form_error").css("display")=="none";
   }

   $("#form-login").submit(function (event) {
      if (!validaForm("login")){
         event.preventDefault();
      }
   });

   $("#form-usr").submit(function (event) {
      if (!validaForm("usr")){
         event.preventDefault();
      }
   });

   $("#form-srv").submit(function (event) {
      if (!validaForm("srv")){
         event.preventDefault();
      }
   });

   $("#mtr_conf_pwd a").click(function (event) {
      event.preventDefault()
      mostrarPwd('#mtr_conf_pwd');
   });

   $('#mtr_pwd a').click(function (event) {
      event.preventDefault()
      mostrarPwd('#mtr_pwd');
   });
   
});