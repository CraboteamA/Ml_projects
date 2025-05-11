// plug this script into index.html by adding
// {% block scripts %}<script src="{{ url_for('static', filename='js/entry.js') }}"></script>{% endblock %}

$(function(){
    const $form = $("form");
    $form.on("submit", function(ev){
      ev.preventDefault();                // stay on page
      $.post("/", $form.serialize())
        .done(()=>{
           showToast("Saved ✔");
           setTimeout(()=>location.reload(), 400);   // reload to refresh streaks
        })
        .fail(()=> showToast("Error!", true));
    });
  
    function showToast(msg, error=false){
      const $t = $(`<div class="toast align-items-center text-bg-${error?'danger':'success'} border-0 position-fixed bottom-0 end-0 m-4">
                      <div class="d-flex">
                        <div class="toast-body">${msg}</div>
                      </div>
                    </div>`).appendTo("body");
      const toast = new bootstrap.Toast($t[0], {delay:1500});
      toast.show();
      toast._element.addEventListener('hidden.bs.toast', ()=> $t.remove());
    }
  });
  