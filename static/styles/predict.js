var x=2;

$(".btn1").click( function() {
  $(".new").before("<div class='box' id='sel0'><label class='count'>Symptom 0 : </label><select class='chname form-control' name='s0'><option>Select Symptom</option>{% for sym in syms %}<option>{{ sym.name }}</option>{% endfor %}</select></div>")
  $(".count").text("Symptom " + x + " : ");

  $(".count").attr("class","");

  y="s"+x;
  $(".chname").attr("name",y);
  $(".chname").removeClass("chname");

  y="sel"+x;
  $("#sel0").attr("id",y);
  x++;
});
