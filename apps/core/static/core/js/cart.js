// var updateBtns = document.getElementsByClassName('add-to-cart')

// for(var i =0; i < updateBtns.length; i++){
//     updateBtns[i].addEventListener('click',function(){
//         var foodId = this.dataset.food
//         var action = this.dataset.action
//         console.log('foodId:',foodId,'action:',action)

//         console.log('USER:',user)
//         if(user === 'AnonymousUser'){
//             console.log('Not logged in')
//         }else{
//             updateUserOrder(foodId, action)
//         }
//     })
// }

// function updateUserOrder(foodId, action){
//     console.log('User is logged in, sending data..')

//     var url = '/restaurant/update_item/'
//     fetch(url, {
//         method:'POST',
//         headers:{
//             'Content-Type':'application/json',
//             'X-CSRFToken':csrftoken,
//         },
//         body:JSON.stringify({'foodId':foodId,'action':action})
//     })
//     .then((response) =>{
//         return response.json()
//     })
//     .then((data) =>{
//         console.log('data:',data)
//     })
// }

    // update cart items 
    $('.update-cart').unbind('click').click(function (e) {
        var fid = $(this).attr("foodId");
        var cart_foodId = $(this).attr("cartfoodid");
        var eml = this.parentNode.children[1];
        var fchild = this.parentNode.children[0];
        var pricechild = this.parentNode.nextElementSibling.children[0];
        var nid = $(fchild).attr("id");
        var action = this.dataset.action
        $.ajax(
          {
            type: "GET",
            url: "/update_cart_item",
            data: {
              foodId: fid,
              action: action,
              cartfoodid: cart_foodId,
            },
            success: function (data) {
                if(data.num===1){
                    $('#'+nid).prop('disabled',true);
                }else{
                    $('#'+nid).removeAttr('disabled');

                }
              eml.innerText = data.num;
              pricechild.innerText ="Rs. "+ data.num * data.food_price;
              document.getElementById('subtotal').innerHTML = `Rs. ${data.subtotal}`;
              document.getElementById('total').innerHTML = `Rs. ${data.total}`;
              document.getElementById('delivery_charge').innerHTML = `Rs. ${data.delivery_charge}`;
            }
          })
      });
                  //   const food_price = document.querySelector('#food-quantity-price');
            //   $.each(data,function(i,item){
            //       food_price.innerText += i.num;
            //   });
                        //   document.getElementById("negative").disabled = false;
    // delete from cart
      $('.remove-cart').unbind('click').click(function (e) {
        var id = $(this).attr("foodId");
        var elm = this;
        $.ajax(
          {
            type: "GET",
            url: "/remove_cart_item",
            data: {
              foodId: id,
            },
            success: function (data) {
                console.log(data);
              $('#cart_no').text(data.cart_count);
              document.getElementById('subtotal').innerHTML = `Rs. ${data.subtotal}`;
              document.getElementById('total').innerHTML = `Rs. ${data.total}`;
              document.getElementById('delivery_charge').innerHTML = `Rs. ${data.delivery_charge}`;
              console.log(data.cart_count);
              if(data.cart_count>0){
                  let mythis = elm.parentNode.parentNode.parentNode;
              $(mythis).fadeOut(500);
              }else if(data.cart_count===0){
                  console.log("I am removing everything")
                      $('#mycartorder').fadeOut(500).hide();
                      $('#emptycart').fadeIn(500).show();
                    //   $('emptycart').show();
                // elm.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.remove();
              }
    
            }
          })
      });
    