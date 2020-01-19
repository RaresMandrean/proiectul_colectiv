function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
var csrftoken = getCookie('csrftoken');
var cont=0;
var isGenerated=false;
var n,m;
        function putPrices1(){
            if(isGenerated===true)
            {
                var minLimit,maxLimit,i,price1;
                minLimit=Number(document.getElementById('minLimit').value);
                maxLimit=Number(document.getElementById('maxLimit').value);
                price1=Number(document.getElementById('price1').value);
                if(maxLimit!==0 && !isNaN(maxLimit) && !isNaN(minLimit) && !isNaN(price1))
                    for(i=minLimit;i<=maxLimit;i++){
                        var gridBlock=getElementByNumber(Number(i));
                        if(gridBlock.length===0) {console.log(gridBlock);document.getElementById("warningPrice1").textContent="The values are incorrect !!";}
                        else {
                            document.getElementById("warningPrice1").textContent="";
   		                    var txtCnt="";
            	            var splitted=gridBlock.textContent.split("\r\n ");
                            var j;
               	            splitted[2]=price1+"$";
           	                for(j=0;j<splitted.length;j++)
                                if(j===splitted.length-1) txtCnt=txtCnt+splitted[j];
                                else txtCnt=txtCnt+splitted[j]+"\r\n ";
            	            gridBlock.textContent=txtCnt;
                        }
                    }
                else {document.getElementById("warningPrice1").textContent="The values are incorrect !!";}
            }
        }
        function putPrices2(){
            if(isGenerated===true)
            {
                var seatsSeparated,i,price2;
                price2=Number(document.getElementById('price2').value);
                seatsSeparated=document.getElementById('seatsSeparated').value;
                seatsSeparated=seatsSeparated.split(",");
	            if(seatsSeparated.length!==0 && !isNaN(price2))
                    for(i=0;i<seatsSeparated.length;i++)
	                {
                        var gridBlock=getElementByNumber(Number(seatsSeparated[i]));
                        if(gridBlock.length===0) {document.getElementById("warningPrice2").textContent="The values are incorrect !!";}
                        else {
                            document.getElementById("warningPrice2").textContent="";
                            var txtCnt="";
                            var splitted=gridBlock.textContent.split("\r\n ");
                            var j;
                            splitted[2]=price2+"$";
                            for(j=0;j<splitted.length;j++)
                                if(j===splitted.length-1) txtCnt=txtCnt+splitted[j];
                                else txtCnt=txtCnt+splitted[j]+"\r\n ";
                            gridBlock.textContent=txtCnt;
                        }
                    }
                else document.getElementById("warningPrice2").textContent="The values are incorrect !!";
            }
        }
        function clik(gridBlockId){
            if(document.getElementById(gridBlockId).style.backgroundColor==="gray") {
                cont=cont+1;document.getElementById(gridBlockId).style.background = "green";
                numberingSeats();
            }
            else if(document.getElementById(gridBlockId).style.backgroundColor==="green") document.getElementById(gridBlockId).style.background = "red";
                else if(document.getElementById(gridBlockId).style.backgroundColor==="red") {
                    cont=cont-1;
                    document.getElementById(gridBlockId).style.background = "gray";
                    var txtCnt="";
                    var splitted=document.getElementById(gridBlockId).textContent.split("\r\n ");
                    var i;
                    splitted[1]=" ";
                    splitted[2]=" ";
                    for(i=0;i<splitted.length;i++)
                        if(i===splitted.length-1) txtCnt=txtCnt+splitted[i];
                        else txtCnt=txtCnt+splitted[i]+"\r\n ";
                    document.getElementById(gridBlockId).textContent=txtCnt;
                    numberingSeats();
                    }
	                else {
                        cont=cont+1;
                        document.getElementById(gridBlockId).style.background = "green";
                        numberingSeats();
                    }
        }
        function numberingSeats(){
            var j;
            var cnt=0;
            var gridItems=document.getElementsByClassName('grid-item');
            for(j=0;j<gridItems.length;j++)
                if(gridItems[j].style.backgroundColor==="green" || gridItems[j].style.backgroundColor==="red") {
                    var txtCnt="";
                    var splitted=gridItems[j].textContent.split("\r\n ");
                    var i;
                    splitted[1]=cnt;
                    for(i=0;i<splitted.length;i++)
                        if(i===splitted.length-1) txtCnt=txtCnt+splitted[i];
                        else txtCnt=txtCnt+splitted[i]+"\r\n ";
                    gridItems[j].textContent=txtCnt;
                    cnt=cnt+1;
                }
        }
        function generateMap(){
            var i,j;
            isGenerated=true;
            n=Number(document.getElementById('height').value);
            m=Number(document.getElementById('width').value);
            var div = document.createElement('div');
            div.className='grid-container';
            div.id='container';
            div.style.display='grid';
            document.getElementsByClassName("mapDiv")[0].appendChild(div);
            var nrColumns="";
            for(i=0;i<m-1;i++)
    	        nrColumns=nrColumns+"auto ";
            nrColumns=nrColumns+"auto";
            document.getElementById("container").style.gridTemplateColumns=nrColumns;
            var idGridBlock=0;
            for(i=0;i<n;i++)
            {
                for(j=0;j<m;j++){
        	        var div1 = document.createElement('div');
                    div1.className='grid-item';
                    div1.setAttribute('style', 'white-space: pre;');
                    div1.textContent=" "+"\r\n  "+"\r\n  ";
                    div1.id="idGridBlock"+idGridBlock;
                    div1.style.backgroundColor="gray";
                    div1.style.border="1px solid rgba(0, 0, 0, 0.8)";
  	            div1.setAttribute("onclick", "clik('"+div1.id+"')");
                document.getElementById('container').appendChild(div1);
	            idGridBlock=idGridBlock+1;
    	        }
            }
        }
        function getElementByNumber(number){
            var gridItems=document.getElementsByClassName('grid-item');
            var x;
            for(x=0;x<gridItems.length;x++)
                if(gridItems[x].style.backgroundColor==="green" || gridItems[x].style.backgroundColor==="red")
                {
                    var splitted=gridItems[x].textContent.split("\r\n ");
                    if(splitted[1]==number) {
                        return gridItems[x];
                    }
                }
            return [];
        }
        function getLocation(){
            console.log("getLocation has been triggered");
            var locationName=document.getElementById("name").value;
            var locationCity=document.getElementById("city").value;
            var locationAddress=document.getElementById("address").value;
            var mapWidth=document.getElementById("width").value;
            var mapHeight=document.getElementById("height").value;
            var arr=[];
            var location={name: locationName, city: locationCity, address: locationAddress, width: Number(mapWidth), height:Number(mapHeight)};
            arr.push(location);
            var seats=document.getElementsByClassName("grid-item");
            for(var i=0;i<seats.length;i++){
                var seat;
                var splitted;
                if(seats[i].style.background==="green"){
                    splitted=seats[i].textContent.split("\r\n ");
                    seat={position:i,location:"",price:Number(splitted[2].substring(0,splitted[2].length-1)),reserved_to:"",special_seat:false}
                    arr.push(seat);
                }
                if(seats[i].style.background==="red") {
                    splitted=seats[i].textContent.split("\r\n ");
                    seat={position:i,location:"",price:Number(splitted[2].substring(0,splitted[2].length-1)),reserved_to:"",special_seat:true}
                    arr.push(seat);
                }
            }
            return JSON.stringify(arr);
        }
        $(document).ready();
        function eventSubmitLocation() {
            $.ajax({
                method: "POST",
                url: "EventAddSeatsLocation",
                dataType: "JSON",
                data: getLocation(),
                success: alert("Location has been added !"),
            });
        }

var selectedSeats = [];
var totalPrice=0;
var isSelected = false;

function clik1(gridBlockId) {
    var txtCnt = "";
    var gridItem = document.getElementById(gridBlockId);
    var splitted = gridItem.textContent.split("\r\n ");
    if (splitted[0] != "res") {
        if (document.getElementById(gridBlockId).style.backgroundColor == "green" && isSelected == false) {
            document.getElementById(gridBlockId).style.background = "red";
            isSelected = true;
            selectedSeats.push(document.getElementById(gridBlockId));
            console.log(gridBlockId);
        } else if (document.getElementById(gridBlockId).style.backgroundColor == "red") {
            document.getElementById(gridBlockId).style.background = "green";
            isSelected = false;
            for (var i = 0; i < selectedSeats.length; i++) {
                if (selectedSeats[i] === document.getElementById(gridBlockId)) {
                    selectedSeats.splice(i, 1);
                }
            }
        }
        if(selectedSeats.length!=0){
            document.getElementById('labelSelectedSeats').innerHTML = selectedSeats[0].textContent.split("\r\n ")[1];
            calculatePriceDetails();
        }
        else{
            document.getElementById('labelSelectedSeats').innerHTML="";
            document.getElementById('totalPrice').innerHTML="";
        }
    }
}

function setMapDetails() {
    var i;
    var elements = document.getElementsByClassName('grid-item');
    for (i = 0; i < elements.length; i++) {
        if (elements[i].style.backgroundColor == "gray") {
            elements[i].style.visibility = 'hidden';
        }
    }
}

function isGreen(id, seats){
    for(var i=0;i<seats.length;i++){
        if(id==seats[i].position && seats[i].special_seat=="false")
            return seats[i];
    }
    return false;
}
function isRed(id,seats){
    for(var i=0;i<seats.length;i++){
        if(id==seats[i].position && seats[i].special_seat=="true")
            return seats[i];
    }
    return false;
}
function isYellow(id,seats,isReserved){
    if(id==isReserved.position)
        return isReserved;
    return false;
}

function generateMapDetails(width,height,seats, isReserved) {
    var n, m, i, j;
    isGenerated = true;
    n = width;
    m = height;
    var nrColumns = "";
    for (i = 0; i < m - 1; i++)
        nrColumns = nrColumns + "auto ";
    nrColumns = nrColumns + "auto";
    var div=document.getElementById("grid-container");
    div.style.gridTemplateColumns = nrColumns;
    div.style.display='grid';
    var idGridBlock = 0;
    var noReserved = 0;
    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
            var id=idGridBlock;
            var div1;
            var isYel=isYellow(id,seats,isReserved);
            if (isReserved!="not reserved" && isYel!=false) {
                div1 = document.createElement('div');
                div1.className = 'grid-item';
                div1.setAttribute('style', 'white-space: pre;');
                div1.textContent = "res " + "\r\n " + noReserved + "\r\n " + isYel.price + "$";
                div1.id = "idGridBlock" + idGridBlock;
                div1.style.background = "yellow";
                div1.style.border = "1px solid rgba(0, 0, 0, 0.8)";
                div.appendChild(div1);
                noReserved = noReserved + 1;
                idGridBlock = idGridBlock + 1;
            }
            else {
                var isGr=isGreen(id,seats);
                if (seats.length!=noReserved && isGr!=false) {
                div1 = document.createElement('div');
                div1.className = 'grid-item';
                div1.setAttribute('style', 'white-space: pre;');
                div1.textContent = " " + "\r\n " + noReserved + "\r\n "+isGr.price+"$";
                div1.id = "idGridBlock" + idGridBlock;
                if(isReserved=="not reserved") div1.setAttribute("onclick", "clik1('" + div1.id + "')");
                div1.style.background = "green";
                div1.style.border="1px solid rgba(0, 0, 0, 0.8)";
                div.appendChild(div1);
                noReserved = noReserved + 1;
                idGridBlock = idGridBlock + 1;
                } else{
                    isRd=isRed(id,seats);
                    if(seats.length!=noReserved && isRd!=false){
                    div1 = document.createElement('div');
                    div1.className = 'grid-item';
                    div1.setAttribute('style', 'white-space: pre;');
                    div1.textContent = "res" + "\r\n " + noReserved + "\r\n "+seats[noReserved].price+"$";
                    div1.id = "idGridBlock" + idGridBlock;
                    if(isReserved=="not reserved")div1.setAttribute("onclick", "clik1('" + div1.id + "')");
                    div1.style.background = "red";
                    div1.style.border="1px solid rgba(0, 0, 0, 0.8)";
                    div.appendChild(div1);
                    noReserved = noReserved + 1;
                    idGridBlock = idGridBlock + 1;
                    } else{
                        div1 = document.createElement('div');
                        div1.className = 'grid-item';
                        div1.setAttribute('style', 'white-space: pre;');
                        div1.textContent = " " + "\r\n  " + "\r\n  ";
                        div1.id = "idGridBlock" + idGridBlock;
                        div1.setAttribute("onclick", "clik1('" + div1.id + "')");
                        div1.style.background = "gray";
                        div.appendChild(div1);
                        idGridBlock = idGridBlock + 1;
                    }
                }
            }
        }
    }
    setMapDetails();
}

function calculatePriceDetails() {
    var gridItems = document.getElementsByClassName('grid-item');
    var index;
    totalPrice=0;
    for (index = 0; index < gridItems.length; index++) {
        if (gridItems[index].style.backgroundColor == "red") {
            var txtCnt = "";
            var splitted = gridItems[index].textContent.split("\r\n ");
            if (splitted[0] != "res") totalPrice = totalPrice + Number(splitted[2].substring(0, splitted[2].length - 1));
        }
    }
    document.getElementById('totalPrice').innerHTML = totalPrice;

}

function getChosenSeat(userid,eventid,locationName){
    var seatToBeAdded=selectedSeats[0];
    splitted=seatToBeAdded.textContent.split("\r\n ");
    result={eventId:eventid,userId:userid,position:seatToBeAdded.id.substring(11,seatToBeAdded.id.length),location:locationName,price:Number(splitted[2].substring(0,splitted[2].length-1))};
    return result
}
function submitChosenSeat(userid,eventid,locationName) {
            $.ajax({
                method: "GET",
                url: "UserEvent",
                dataType: "JSON",
                data: getChosenSeat(userid,eventid,locationName),
                success: alert("Location has been added !"),
            });
        }