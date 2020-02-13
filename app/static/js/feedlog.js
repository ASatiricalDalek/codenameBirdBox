    setInterval("my_function();",500);
    function my_function(){
      $('#feedLog').load(location.href + ' #feedLog');
    }

    // BLACK MAGIC FUCKERY