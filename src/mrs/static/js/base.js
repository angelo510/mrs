import ScrollReveal from 'scrollreveal'
import '../sass/base.sass'
import '../sass/landing.sass'
import '../sass/base.sass'
import '../sass/form.sass'
import '../sass/animations.sass'
import '../sass/index.sass'
import '../sass/faq.sass'
import '../sass/caroussel.sass'
import './mrsrequest'
import './contact'
import initStatistics from './statistics.js'

// Preact imports
import { h as React, render } from 'preact'
import Header from './components/Header.js'
import Carousel from './components/Caroussel.js'


(() => {
  let body = document.querySelector('body')

  const renderHeader = isFat => render(<Header isFat={ isFat } />, document.getElementById('header'))
  const renderCarousel = () => render(<Carousel />, document.getElementById('caroussel'))

  // show correct header based on path
  if(body.classList.contains('index')) {
    const sr = ScrollReveal()
    sr.reveal('.scroll-reveal')
    renderHeader(false)
    renderCarousel()
  } else {
    renderHeader(true)
  }

  // use bodyclass to detect statistics
  if(body.classList.contains('statistics')) {
    initStatistics()
  }

})()
