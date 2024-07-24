import{j as e,w as h,aO as x,d3 as b,d4 as f,v as n,d5 as r,d6 as y,d7 as P,r as v,b as E,d8 as R}from"./vendor-DPvSDRn3.js";import{t as z,a4 as L}from"./vendor-arizeai-CkvPT67c.js";import{L as $,E as j,h as k,M as w,a as d,D as I,d as A,b as S,e as O,P as C,c as F,f as T,p as D,g as c,i as M,j as N,k as p,l as B,m,n as g,o as q,q as G,r as W,s as K,t as Y,A as Z,F as _}from"./pages-hdjlFZhO.js";import{aY as H,d as J,R as Q,aZ as U,a_ as V}from"./components-DeS0YEmv.js";import"./vendor-three-DwGkEfCM.js";import"./vendor-recharts-5jlNaZuF.js";import"./vendor-codemirror-Cqwpwlua.js";(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const a of document.querySelectorAll('link[rel="modulepreload"]'))i(a);new MutationObserver(a=>{for(const t of a)if(t.type==="childList")for(const l of t.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&i(l)}).observe(document,{childList:!0,subtree:!0});function u(a){const t={};return a.integrity&&(t.integrity=a.integrity),a.referrerPolicy&&(t.referrerPolicy=a.referrerPolicy),a.crossOrigin==="use-credentials"?t.credentials="include":a.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function i(a){if(a.ep)return;a.ep=!0;const t=u(a);fetch(a.href,t)}})();function X(){return e(x,{styles:o=>h`
        body {
          background-color: var(--ac-global-color-grey-75);
          color: var(--ac-global-text-color-900);
          font-family: "Roboto";
          font-size: ${o.typography.sizes.medium.fontSize}px;
          margin: 0;
          #root,
          #root > div[data-overlay-container="true"],
          #root > div[data-overlay-container="true"] > .ac-theme {
            height: 100vh;
          }
        }

        /* Remove list styling */
        ul {
          display: block;
          list-style-type: none;
          margin-block-start: none;
          margin-block-end: 0;
          padding-inline-start: 0;
          margin-block-start: 0;
        }

        /* A reset style for buttons */
        .button--reset {
          background: none;
          border: none;
          padding: 0;
        }
        /* this css class is added to html via modernizr @see modernizr.js */
        .no-hiddenscroll {
          /* Works on Firefox */
          * {
            scrollbar-width: thin;
            scrollbar-color: var(--ac-global-color-grey-300)
              var(--ac-global-color-grey-400);
          }

          /* Works on Chrome, Edge, and Safari */
          *::-webkit-scrollbar {
            width: 14px;
          }

          *::-webkit-scrollbar-track {
            background: var(--ac-global-color-grey-100);
          }

          *::-webkit-scrollbar-thumb {
            background-color: var(--ac-global-color-grey-75);
            border-radius: 8px;
            border: 1px solid var(--ac-global-color-grey-300);
          }
        }

        :root {
          --px-blue-color: ${o.colors.arizeBlue};

          --px-flex-gap-sm: ${o.spacing.margin4}px;
          --px-flex-gap-sm: ${o.spacing.margin8}px;

          --px-section-background-color: ${o.colors.gray500};

          /* An item is a typically something in a list */
          --px-item-background-color: ${o.colors.gray800};
          --px-item-border-color: ${o.colors.gray600};

          --px-spacing-sm: ${o.spacing.padding4}px;
          --px-spacing-med: ${o.spacing.padding8}px;
          --px-spacing-lg: ${o.spacing.padding16}px;

          --px-border-radius-med: ${o.borderRadius.medium}px;

          --px-font-size-sm: ${o.typography.sizes.small.fontSize}px;
          --px-font-size-med: ${o.typography.sizes.medium.fontSize}px;
          --px-font-size-lg: ${o.typography.sizes.large.fontSize}px;

          --px-gradient-bar-height: 8px;

          --px-nav-collapsed-width: 45px;
          --px-nav-expanded-width: 200px;
        }

        .ac-theme--dark {
          --px-primary-color: #9efcfd;
          --px-primary-color--transparent: rgb(158, 252, 253, 0.2);
          --px-reference-color: #baa1f9;
          --px-reference-color--transparent: #baa1f982;
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
        .ac-theme--light {
          --px-primary-color: #00add0;
          --px-primary-color--transparent: rgba(0, 173, 208, 0.2);
          --px-reference-color: #4500d9;
          --px-reference-color--transparent: rgba(69, 0, 217, 0.2);
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
      `})}const ee=b(f(n(r,{path:"/",element:e($,{}),errorElement:e(j,{}),children:[e(r,{index:!0,loader:k}),n(r,{path:"/model",handle:{crumb:()=>"model"},element:e(w,{}),children:[e(r,{index:!0,element:e(d,{})}),e(r,{element:e(d,{}),children:e(r,{path:"dimensions",children:e(r,{path:":dimensionId",element:e(I,{}),loader:A})})}),e(r,{path:"embeddings",children:e(r,{path:":embeddingDimensionId",element:e(S,{}),loader:O,handle:{crumb:o=>o.embedding.name}})})]}),n(r,{path:"/projects",handle:{crumb:()=>"projects"},element:e(C,{}),children:[e(r,{index:!0,element:e(F,{})}),n(r,{path:":projectId",element:e(T,{}),loader:D,handle:{crumb:o=>o.project.name},children:[e(r,{index:!0,element:e(c,{})}),e(r,{element:e(c,{}),children:e(r,{path:"traces/:traceId",element:e(M,{})})})]})]}),n(r,{path:"/datasets",handle:{crumb:()=>"datasets"},children:[e(r,{index:!0,element:e(N,{})}),n(r,{path:":datasetId",loader:p,handle:{crumb:o=>o.dataset.name},children:[n(r,{element:e(B,{}),loader:p,children:[e(r,{index:!0,element:e(m,{}),loader:g}),e(r,{path:"experiments",element:e(m,{}),loader:g}),e(r,{path:"examples",element:e(q,{}),loader:G,children:e(r,{path:":exampleId",element:e(W,{})})})]}),e(r,{path:"compare",handle:{crumb:()=>"compare"},loader:K,element:e(Y,{})})]})]}),e(r,{path:"/apis",element:e(Z,{}),handle:{crumb:()=>"APIs"}})]})),{basename:window.Config.basename});function re(){return e(y,{router:ee})}function oe(){return e(H,{children:e(ae,{})})}function ae(){const{theme:o}=J();return e(L,{theme:o,children:e(P,{theme:z,children:n(E.RelayEnvironmentProvider,{environment:Q,children:[e(X,{}),e(_,{children:e(U,{children:e(v.Suspense,{children:e(V,{children:e(re,{})})})})})]})})})}const te=document.getElementById("root"),ne=R.createRoot(te);ne.render(e(oe,{}));
