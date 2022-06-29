const searchField=document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
tableOutput.style.display = "none";
const tbody = document.querySelector(".table-body");


searchField.addEventListener('keyup',(e)=>{
    const searchValue= e.target.value;
    if(searchValue.trim().length>0){
        console.log("searchValue",searchValue);
        tbody.innerHTML = "";
        fetch("/restaurants/search-food",{
            body: JSON.stringify({ searchText: searchValue}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data",data);
            appTable.style.display = "none"
            tableOutput.style.display="block";
            console.log("data.length",data.length);

            if(data.length === 0){
                tableOutput.innerHTML="No results found !!";
                // $(document).ready(function(){
                //     setInterval(function(){
                //           $("#here").load(window.location.href + " #here" );
                //     }, 200);
                //     });
                searchField.addEventListener("keydown", function(event) {
                    if (event.keyCode == 8) {
                        window.location.reload();
                    }
                  });
            }else{
                data.forEach((item,i) => {
                    tbody.innerHTML += `
                    <tr>
                    <td>${i}</td>
                    <td><img src="${item.food_image}"></td>
                    <td>${item.food_name}</td>
                    <td>${item.food_price}</td>
                    <td>${item.menu}</td>
                    <td>${item.food_description}</td>
                    <td>
                                <a href="edit_food' food.id" class="btn text-secondary px-0" id="upid">
                                    <i class="fa fa-edit" style="font-size: 25px; color: blueviolet;text-shadow:2px 2px 4px #000000;"></i>
                                </a> |
                                <a href="delete_food food.id" class="btn text-secondary px-0" id="delid">
                                    <i class="fa fa-trash" style="font-size: 25px; color:red; text-shadow:2px 2px 4px black;"></i>
                                </a>
                            </td>
                    </tr>`;
                });
            }
            tableOutput.style.display="block";
        });
    }else{
        tableOutput.style.display="none";
        appTable.style.display="block";
    }
});