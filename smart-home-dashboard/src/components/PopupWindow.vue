<script setup>

</script>

<template>
    <div class="modal-wrapper" aria-modal="true"
      role="dialog" tabindex="-1">
      <div class="inner">
           <button class="close-btn" @click="$emit('closePopup')">
               <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 256 256">
               <path fill="currentColor"
                   d="M208.49 191.51a12 12 0 0 1-17 17L128 145l-63.51 63.49a12 12 0 0 1-17-17L111 128L47.51 64.49a12 12 0 0 1 17-17L128 111l63.51-63.52a12 12 0 0 1 17 17L145 128Z" />
               </svg>
           </button>

           <slot></slot>
      </div>
  </div>

</template>

<style lang="scss" scoped>
.modal-wrapper {
       position: fixed;
       left: 0;
       top: 0;
       z-index: 500;
       width: 100vw;
       height: 100vh;
       background: rgba(0, 0, 0, 0.2);
       display: grid;
       place-items: center;
       color: #000;
  
       .inner {
       background-color: white;
       padding: 30px;
       border-radius: 12px;
       display: flex;
       flex-direction: column;
       position: relative;
       max-width: 600px;
       width: 90%;
  
       h3 {
           font-size: 16px;
           font-weight: 700;
           line-height: 21px;
           margin-bottom: 20px;
       }
  
       .close-btn {
           position: absolute;
           top: 15px;
           right: 15px;
           cursor: pointer;
           background-color: #fff;
       }
  
       .form {
           display: flex;
           flex-direction: column;
           max-width: 100%;


           label {
           font-size: 12px;
           font-weight: 500;
           line-height: 16px;
           letter-spacing: 0em;
           text-align: left;
           }


           input,
           select,
           textarea {
           font-size: 12px;
           font-weight: 400;
           line-height: 16px;
           letter-spacing: 0em;
           text-align: left;
           border: 1px solid #C2C2C2;
           border-radius: 4px;
           padding: 8px 12px;
           margin-top: 5px;


           &::placeholder {
               color: #A6A6A6;
           }
           }
  
          
  
           .btn {
           width: fit-content;
           padding-inline: 23px;
           }
       }
       }
   }


</style>