 var zip_inflate_codes = function(buff, off, size) {
        var e;
        var t;
        var n;
        if (size == 0) {
            return 0
        }
        n = 0;
        for (; ; ) {
            zip_NEEDBITS(zip_bl);
            t = zip_tl.list[zip_GETBITS(zip_bl)];
            e = t.e;
            while (e > 16) {
                if (e == 99) {
                    return -1
                }
                zip_DUMPBITS(t.b);
                e -= 16;
                zip_NEEDBITS(e);
                t = t.t[zip_GETBITS(e)];
                e = t.e
            }
            zip_DUMPBITS(t.b);
            if (e == 16) {
                zip_wp &= zip_WSIZE - 1;
                buff[off + n++] = zip_slide[zip_wp++] = t.n;
                if (n == size) {
                    return size
                }
                continue
            }
            if (e == 15) {
                break
            }
            zip_NEEDBITS(e);
            zip_copy_leng = t.n + zip_GETBITS(e);
            zip_DUMPBITS(e);
            zip_NEEDBITS(zip_bd);
            t = zip_td.list[zip_GETBITS(zip_bd)];
            e = t.e;
            while (e > 16) {
                if (e == 99) {
                    return -1
                }
                zip_DUMPBITS(t.b);
                e -= 16;
                zip_NEEDBITS(e);
                t = t.t[zip_GETBITS(e)];
                e = t.e
            }
            zip_DUMPBITS(t.b);
            zip_NEEDBITS(e);
            zip_copy_dist = zip_wp - t.n - zip_GETBITS(e);
            zip_DUMPBITS(e);
            while (zip_copy_leng > 0 && n < size) {
                zip_copy_leng--;
                zip_copy_dist &= zip_WSIZE - 1;
                zip_wp &= zip_WSIZE - 1;
                buff[off + n++] = zip_slide[zip_wp++] = zip_slide[zip_copy_dist++]
            }
            if (n == size) {
                return size
            }
        }
        zip_method = -1;
        return n
    };
    var zip_inflate_stored = function(buff, off, size) {
        var n;
        n = zip_bit_len & 7;
        zip_DUMPBITS(n);
        zip_NEEDBITS(16);
        n = zip_GETBITS(16);
        zip_DUMPBITS(16);
        zip_NEEDBITS(16);
        if (n != ((~zip_bit_buf) & 65535)) {
            return -1
        }
        zip_DUMPBITS(16);
        zip_copy_leng = n;
        n = 0;
        while (zip_copy_leng > 0 && n < size) {
            zip_copy_leng--;
            zip_wp &= zip_WSIZE - 1;
            zip_NEEDBITS(8);
            buff[off + n++] = zip_slide[zip_wp++] = zip_GETBITS(8);
            zip_DUMPBITS(8)
        }
        if (zip_copy_leng == 0) {
            zip_method = -1
        }
        return n
    };
    var zip_inflate_fixed = function(buff, off, size) {
        if (zip_fixed_tl == null) {
            var i;
            var l = new Array(288);
            var h;
            for (i = 0; i < 144; i++) {
                l[i] = 8
            }
            for (; i < 256; i++) {
                l[i] = 9
            }
            for (; i < 280; i++) {
                l[i] = 7
            }
            for (; i < 288; i++) {
                l[i] = 8
            }
            zip_fixed_bl = 7;
            h = new zip_HuftBuild(l,288,257,zip_cplens,zip_cplext,zip_fixed_bl);
            if (h.status != 0) {
                alert("HufBuild error: " + h.status);
                return -1
            }
            zip_fixed_tl = h.root;
            zip_fixed_bl = h.m;
            for (i = 0; i < 30; i++) {
                l[i] = 5
            }
            zip_fixed_bd = 5;
            h = new zip_HuftBuild(l,30,0,zip_cpdist,zip_cpdext,zip_fixed_bd);
            if (h.status > 1) {
                zip_fixed_tl = null;
                alert("HufBuild error: " + h.status);
                return -1
            }
            zip_fixed_td = h.root;
            zip_fixed_bd = h.m
        }
        zip_tl = zip_fixed_tl;
        zip_td = zip_fixed_td;
        zip_bl = zip_fixed_bl;
        zip_bd = zip_fixed_bd;
        return zip_inflate_codes(buff, off, size)
    };
