import Vue from 'vue'
import Vuex from 'vuex'
import Api from "@/services/api"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    images:[]
  },
  mutations: {
    ADD_IMAGE(state, image){
      let images = state.images.concat(image);
      state.images = images;
    }
  },
  actions: {
    async Post_image({commit},image){
      try{
        let response = await Api().post('/',image);
        console.log(response);
        let to_add = response.data;
        commit('ADD_IMAGE',to_add);
        return to_add;
      }
      catch{
        return{error: "Hubo un error al subir la imagen"}
      }
    }
  },
  modules: {
  }
})
