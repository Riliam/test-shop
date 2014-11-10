$(document).ready(function() {

  $("#categories-tree").jstree({
    "core": { 
      "animation": 0,
      "themes": {
        "icons": false
      }    
    },
    "plugins": ["themes", "ui", "state"]
    // nodes and leafs as links
    }).bind("select_node.jstree", function (e, data) {
      $('#jstree').jstree('save_state');
    }).on("activate_node.jstree", function (e, data) {
      document.location.href = data.node.a_attr.href;
  });


  $("#product-rating").on('rating.change', function(event, value, caption){
    var pid = $(this).attr("data-pid");
    $.ajax({
      type: "GET",
      url: "/rate_product",
      data: {product_id: pid, value: value},
      success: function(data){
        $('#id-product-rating').html(data.rating);
        $('#id-product-raters').html(data.raters);
        $('#product-rating').rating('update', data.rating);
        $('#product-rating').rating('refresh', {'disabled': true});
      },
      error: function(data){
        alert("Error");
      }
    });
  });

  $("#add-to-cart-button").on("click", function(){
    var product_id = $(this).attr("data-pid");
    $.ajax({
      type: "GET",
      url: "/add/" + product_id,
      data: {},
      success: function(data){
        $("#products-in-cart").html(data["products_in_cart"]);
        $("#cart-total-sum").html(data["cart_total_sum"]);
      },
      error: function(data){
        alert("Error");
      }
    });
  });

  $('#backcall-button').on("click", function() { // catch the form's submit event
      $('.feedback').removeClass('alert alert-success alert-warning').addClass('alert alert-info').html('Подождите...');
      $.ajax({ // create an AJAX call...
          data: $('#backcall-form').serialize(), // get the form data
          type: $('#backcall-form').attr('method'), // GET or POST
          url: $('#backcall-form').attr('action'), // the file to call
          success: function(response) { // on success..
            $('.feedback').removeClass('alert-info').addClass('alert-success').html('Спасибо за заявку, ' + $('#back-call-name').val() + ". Наш менеджер скоро с вами свяжется.");
            $('#back-call-name').val('');
            $('#back-call-phonenumber').val('');
          },
          error: function(response) {
            $('.feedback').removeClass('alert-info').addClass('alert-warning').html('Что-то пошло не так. Заявка не отправлена');
          }
      });
      return false;
  });

  $('#id-show-cart-modal').on("click", function() {
    $.ajax({
      url: '/update-cart',
      type: 'get',
      success: function(response) {
        $('.cart-products-table').html(response.table_html);
      },
      error: function(response) {
        alert("Error");
      }
    });
  });
}); 
