


function load_app_section(sectionId){
    // Remove all active sctions
    const sections = document.querySelectorAll('.app-section') // returns node list of all sections
    sections.forEach(section => {
        section.classList.remove("active-section");
    });

    // Add the desired active-section 
    document.querySelector(`#${sectionId}`).classList.add('active-section')
    if (sectionId == "session-config"){
        load_drawing_session_config_section("session-pics")
        set_active_tab("pic-tab", "htab")
    }
}

function load_drawing_session_config_section(sectionId){
    // Remove all active sctions
    console.log("loading section ", sectionId)
    const sections = document.querySelectorAll('.drawing-session-config') // returns node list of all sections
    sections.forEach(section => {
        section.classList.remove("active-config-section");
    });

    // Add the desired active-section 
    document.querySelector(`#${sectionId}`).classList.add('active-config-section')    
}


function set_active_tab(tabId,tabtype){
    // tabId the tab to activate, tabtype the htabs or vtabs
    deactivate_tabs(tabtype)
    // Add active-tab to element with tabId
    console.log("targetting => ", tabId)
    const target = document.querySelector(`#${tabId}`)
    target.classList.add("active-tab")
}


function deactivate_tabs(tabtype){
    // tabtype ie htab or vtab
    const tabs = document.querySelectorAll(`.${tabtype}`)
    tabs.forEach(tab => {
        tab.classList.remove("active-tab")
    })
}



// Clicking a link in the nav activates the corrosponding section in the center panel
function add_nav_panel_links(){
    console.log("adding nav links")

    // get nav link elements and add event listeners
    console.log("Adding nav links")
    const navLinks = document.querySelectorAll(".nav-item");
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const sectionId = link.getAttribute('data-section');
            //deactivate_tabs("vtab")
            load_app_section(sectionId);
        })
    })
    console.log("done")



    console.log("adding home splat")
    const homeSplat = document.getElementById("splat1-svg-group")
    homeSplat.addEventListener("click", () => {
        const sectionId = homeSplat.getAttribute("data-section")
        load_app_section(sectionId)
        // activate pic-tab
        set_active_tab("pic-tab")

    })
    console.log("done")

    console.log("Adding Get Drawing link")
    const getDrawing = document.getElementById("get-drawing");
    getDrawing.addEventListener("click", () => {
        const sectionId = homeSplat.getAttribute("data-section")
        console.log("Section Id = ", sectionId)
        load_app_section(sectionId)
       // activate pic-tab
        set_active_tab("pic-tab","htab")
    })
    console.log("done")


    
}

function add_account_link(){
    console.log("Adding Account Link")
    const user_account = document.getElementById("user-account");
    user_account.addEventListener("click", () => {
        const sectionId = user_account.getAttribute("data-section")
        console.log("sectionId:",sectionId)
        load_app_section(sectionId)
    })
    console.log("done")
}

// This adds all vtabs
function add_nav_tabs(){
    const navTabs = document.querySelectorAll(".vtab");
    navTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const sectionId = tab.getAttribute("data-section");
            load_app_section(sectionId)
            // get associated tabId
            const tabId = tab.id
            set_active_tab(tabId, "vtab")
        })
    })
}




function add_authentication_links(){
    // Authentication Links Event Handlers
    const auth_links = document.querySelectorAll(".auth-link")
    auth_links.forEach(link => {
        link.addEventListener("click", () => {
            const sectionId = link.getAttribute("data-section")
            load_app_section(sectionId) 
        })
    })
}


function add_drawing_session_config_tabs(){
    console.log("adding tabs")
    const drawing_session_tabs = document.querySelectorAll(".htab")
    drawing_session_tabs.forEach(tab => {
        tab.addEventListener("click",() => {
            const section_id = tab.getAttribute("data-section")
            load_drawing_session_config_section(section_id)
            set_active_tab(tab.id, "htab")

        })

    })
}

function setupFormSubmitPulse() {
    console.log("Setup Pulse")
  const submitButton = document.querySelector('.inksplat-submit');

  function triggerPulse() {
    submitButton.classList.add('pulse');
    // Remove the class after the animation duration (700ms)
    setTimeout(() => {
      submitButton.classList.remove('pulse');
    }, 700);
  }

  // Trigger immediately on load
  triggerPulse();

  // Repeat every 30 seconds
  setInterval(triggerPulse, 5000);
}


/*********************************************************************** */
/*
/* Main Javascript Function on DOM Content Loaded
/*
/*
/*********************************************************************** */
document.addEventListener('DOMContentLoaded', function(){
    console.log("####### DOM LOADED ############");
    // load default active-section
    const state_data = document.getElementById("state-data")
    const sectionId = state_data.getAttribute("data-section");
    console.log("active_section: ",  sectionId)
    // switch off all sections ie remove active-section class
    document.querySelectorAll(".app-section").forEach(sec => {
            sec.classList.remove("active-section");
    });
    const targetSection = document.getElementById(sectionId);
    targetSection.classList.add("active-section");



    // Add Event Listeners
    add_nav_panel_links()
    add_authentication_links()
    add_account_link()
    //add_nav_tabs()
    add_drawing_session_config_tabs()

    setupFormSubmitPulse()
  
    // handle session-config tabs so that it works within the session config section
    // ie selecting a sesssion-config section like session-pics doesnt switch off the session-config section 
    // all together

    // Add Extras Panel Event Listeners

    // Add Main Panel Event Listeners

})