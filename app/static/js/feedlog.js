    setInterval("my_function();",1000);
    function my_function(){
      $('#feedLog').load(location.href + ' #feedLog');
    }

    // BLACK MAGIC FUCKERY