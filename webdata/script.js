async function triggerApiCallAndResponse() {
    // grab the input 
    const sub = document.getElementById('submitBox');
    console.log(sub);
    // if (!navigator.geolocation) {
    //   throw new Error("What aguppun")
    // } else {
    //   navigator.geolocation.getCurrentPosition(suc => {
    //     //"getCurrentPosition"
    //   }, err => {
    //     throw new Error("")
    //   })
    // }
    const bgh = await fetch('/runsearch', {
      method: 'POST',
      body: JSON.stringify({
        sign_text: sub.value,
        lat: 0,
        lon: 0,
        time: Date.now()
      })
    });
    const data = await bgh.json();
    const adjuster = document.getElementById('main')
      console.log("dd2")
    if (adjuster) {
      adjuster.classList.remove('nil-response-provided');
      adjuster.classList.remove('yes-response-provided');
      adjuster.classList.remove('no-response-provided');
    }
    console.log("dd1")
    if (data.canpark && data.canpark !== 'false') {
    console.log("dd13", data);
      adjuster.classList.add('yes-response-provided');
    } else {
    console.log("dd13")
      adjuster.classList.add('no-response-provided');
    }
    // let dr = document.querySelector(`.boxes-hidden.${data.can_park ? 'yes' : 'no'}-response`)
    // while (dr) {
    //   dr.classList.remove('boxes-hidden');
    //   dr = document.querySelector(`.boxes-hidden.${data.can_park ? 'yes' : 'no'}-response`)
    // }

    ////////

}

  
