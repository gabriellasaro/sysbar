function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function save_product(data) {
    if (data.length!=2){
        alert("Erro ao adicionar ao carrinho!");
        return false;
    }
    result = getCookie("dcart");
    if (result==""){
        info = '{"cart":[{"ID_product":'+data[0]+',"shared":'+data[1]+', "quant":1}]}';
        document.cookie = "dcart="+info+";path=/";
        alert("Produto adicionado no carrinho!");
        return true;
    }else{
        jr = JSON.parse(result);
        quant = 1;
        for (let i=0; i<jr['cart'].length; i++) {
            console.log(jr['cart'][i]['ID_product']+" - "+data[0]);
            console.log(jr['cart'][i]['shared']+" - "+data[1]);
            if (jr['cart'][i]['ID_product']==data[0]){
                if (jr['cart'][i]['shared']==data[1]){
                    quant += jr['cart'][i]['quant'];
                    id = i;
                    break;
                }
            }
        }
        if (quant>1){
            jr["cart"][id]["quant"] = quant;
        }else{
            jr["cart"].push({
                "ID_product":data[0],
                "shared":data[1],
                "quant":quant
            });
        }
        document.cookie = "dcart="+JSON.stringify(jr)+";path=/";
        alert("Produto adicionado no carrinho!");
        return true;
    }
}