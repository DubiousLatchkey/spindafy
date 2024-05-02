# DOOM via Spinda

This is my fork of Spindafy by [Ovidios](https://github.com/Ovidios) combinining it with DOOM on checkboxes by [healeycodes](https://github.com/healeycodes) to bring you DOOM rendered on Spindas.

My method recreates uses pregenerated Spindas from Spindafy to tile a canvas object in webassembly DOOM.  Rather than using a genetic approach like Spindafy, this method takes advantage of the fact that the 4 dots on Spinda each have their own area on the Spinda in which they can generate.  By assigning each Spinda dot a pixel, we can get a reasonable image fast enough to render the game.  Maybe later I can make each Spinda represent 8 or even 16 pixels, but not today.

To run, follow the instructions of the DOOM via checkboxes README below.


# READMEs of the Other Projects

## :joystick: DOOM via Checkboxes
> My blog post: [DOOM Rendered via Checkboxes](https://healeycodes.com/doom-rendered-via-checkboxes)

<br>

![Preview image of DOOM/DOOM checkboxes](https://github.com/healeycodes/doom-checkboxes/blob/main/preview.png)

<br>

[Play it now](https://healeycodes.github.io/doom-checkboxes/) (desktop Chrome/Edge only).

## The Pitch

> I don't think you can really say you've exhaused this until you can run DOOM rendered with checkboxes.

— a commenter wrote [on Hacker News](https://news.ycombinator.com/item?id=28826839)

<br>

Bryan Braun gave us [Checkboxland](https://www.bryanbraun.com/checkboxland/), a unique library for rendering text, shapes, and video, via a grid of checkboxes.

Id software gave us [DOOM](https://en.wikipedia.org/wiki/Doom_(franchise)).

Cornelius Diekmann gave us [DOOM via WebAssembly](https://github.com/diekmann/wasm-fizzbuzz).

Today, I'm pleased to stand on top of these giants' shoulders, and give you DOOM via Checkboxes.

## How

DOOM runs via WebAssembly in a hidden `<canvas>`. I use [HTMLCanvasElement.captureStream()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/captureStream) to turn this into a MediaStream. A `<video>` element displays this MediaStream and is then consumed by [renderVideo](https://www.bryanbraun.com/checkboxland/#rendervideo) from Checkboxland.

Optionally, the `<video>` element can be hidden as well. However, test users were unable to exit the main menu without the aid of the original hi-res DOOM.

Our screen is a 160 by 100 grid of native checkboxes. Higher resolutions work but FPS drops off dramatically.

```js
const cbl = new Checkboxland({
  dimensions: "160x100",
  selector: "#checkboxes",
});
```

The cursed CSS property [zoom](https://developer.mozilla.org/en-US/docs/Web/CSS/zoom) is used to shrink the checkboxes down. `transform: scale(x)` resulted in worse performance, and worse visuals. Unfortunately, this means that Firefox users need to manually zoom out.

> Non-standard: This feature is non-standard and is not on a standards track. Do not use it on production sites facing the Web: it will not work for every user.

Key events are forwarded to the hidden `<canvas>` to avoid focus issues.

```js
const forwardKey = (e, type) => {
  const ev = new KeyboardEvent(type, {
    key: e.key,
    keyCode: e.keyCode,
  });
  canvas.dispatchEvent(ev);
};

document.body.addEventListener("keydown", function (e) {
  forwardKey(e, "keydown");
});

document.body.addEventListener("keyup", function (e) {
  forwardKey(e, "keyup");
});
```

While the `.wasm` is downloaded and processed, the grid displays a message via [print](https://www.bryanbraun.com/checkboxland/#print).

![DOOM WebAssembly loading..](https://github.com/healeycodes/doom-checkboxes/blob/main/loading.png)

Afterwards, the user is instructed to click anywhere (a user action is required so that the `<video>` can be programmatically played) and the game begins!

## Development

```bash
python dev.py
```

Edit files, refresh.

# Spindafy
This is a simple script to find a personality value (PID) that most closely matches a target image when applied as a pattern to the Pokémon Spinda!

It consists of the following files:
- ``spindafy.py`` defines the ``SpindaConfig`` class, representing a Spinda point configuration. It also contains a method to render the pattern to a PIL Image, compare it to a target image, an to check whether a pixel is within a spot's area.
- ``spinda_optimizer.py`` defines a *very* simple genetic algorithm to try and find a good PID for a given input image.
- ``spinda_anim.py`` just runs the genetic algorithm on a number of files in a given directory and writes the results to a different directory (both given as command line arguments.) See [this YouTube video](https://www.youtube.com/watch?v=ZzsBIfA6iog) for an example.
- ``large_spinda.py`` implements a super naive and *very* slow spinda mosaic generator. Example:
  ![a mosaic of spinda forming a yin and yang symbol](res/test_large_result.png)
- ``large_spinda_anim.py`` is the mosaic equivalent of ``spinda_anim.py``.